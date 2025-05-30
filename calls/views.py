from django.shortcuts import render
import logging
import os
import time
from datetime import datetime
from django.http import HttpResponse, FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings

from .models import Call
from .serializers import (
    CallSerializer, InitiateCallSerializer,
    EndCallSerializer, UploadRecordingSerializer
)
from .twilio_service import TwilioService
from .ai_service import AIService
from leads.models import Lead
from utils.response_template import custom_success_response, custom_error_response

logger = logging.getLogger(__name__)


class CallViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='history')
    def get_call_history(self, request):
        try:
            logger.info("Fetching call history", extra={"user": request.user})
            calls = Call.objects.filter(user=request.user)
            serializer = CallSerializer(calls, many=True)
            return custom_success_response(serializer.data)
        except Exception as e:
            logger.error("Error fetching call history", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['POST'], url_path='initiate')
    def initiate_call(self, request):
        try:
            logger.info("Initiating call", extra={"user": request.user})
            serializer = InitiateCallSerializer(data=request.data)

            if serializer.is_valid():
                phone_number = serializer.validated_data['phone_number']
                lead_id = serializer.validated_data.get('lead_id')

                # Get lead if provided
                lead = None
                if lead_id:
                    try:
                        lead = Lead.objects.get(
                            id=lead_id, created_by=request.user)
                    except Lead.DoesNotExist:
                        return custom_error_response(
                            message="Lead not found",
                            status_code=status.HTTP_404_NOT_FOUND
                        )

                # Create call record
                call = Call.objects.create(
                    user=request.user,
                    lead=lead,
                    phone_number=phone_number,
                    status='initiated'
                )

                # Initiate Twilio call
                twilio_service = TwilioService()
                twilio_result = twilio_service.initiate_call(phone_number)

                if twilio_result['success']:
                    call.twilio_call_sid = twilio_result['call_sid']
                    call.status = 'ringing'
                    call.save()

                    response_data = CallSerializer(call).data
                    return custom_success_response(
                        response_data,
                        status.HTTP_201_CREATED
                    )
                else:
                    call.status = 'failed'
                    call.save()
                    return custom_error_response(
                        message=f"Failed to initiate call: {twilio_result['error']}",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

            return custom_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error initiating call", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'], url_path='end')
    def end_call(self, request, pk=None):
        try:
            logger.info(f"Ending call {pk}", extra={"user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            serializer = EndCallSerializer(data=request.data)
            if serializer.is_valid():
                duration = serializer.validated_data['duration']
                notes = serializer.validated_data.get('notes', '')

                # End Twilio call if call_sid exists
                if call.twilio_call_sid:
                    twilio_service = TwilioService()
                    twilio_service.end_call(call.twilio_call_sid)

                # Update call record
                call.end_time = timezone.now()
                call.duration = duration
                call.notes = notes
                call.status = 'completed'
                call.save()

                response_data = CallSerializer(call).data
                return custom_success_response(response_data)

            return custom_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error ending call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['PATCH'], url_path='notes')
    def update_notes(self, request, pk=None):
        try:
            logger.info(f"Updating notes for call {pk}", extra={
                        "user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            notes = request.data.get('notes', '')

            # Update call notes
            call.notes = notes
            call.save()

            response_data = CallSerializer(call).data
            return custom_success_response(response_data)

        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating notes for call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'], url_path='download-recording')
    def download_recording(self, request, pk=None):
        try:
            logger.info(f"Downloading recording for call {pk}", extra={
                        "user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            if not call.twilio_call_sid:
                return custom_error_response(
                    message="No Twilio call ID found for this call",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            twilio_service = TwilioService()

            # Get recordings for this call
            recordings_result = twilio_service.get_call_recordings(
                call.twilio_call_sid)

            if not recordings_result['success']:
                return custom_error_response(
                    message=f"Failed to fetch recordings: {recordings_result['error']}",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            recordings = recordings_result['recordings']
            if not recordings:
                return custom_error_response(
                    message="No recordings found for this call. Recording may still be processing.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Use the first recording (there should typically be only one)
            recording = recordings[0]
            recording_sid = recording['sid']

            # Generate filename: phonenumber_timestamp.mp3
            timestamp = int(time.time())
            filename = f"{call.phone_number.replace('+', '')}_{timestamp}.mp3"
            file_path = os.path.join('recordings', filename)
            full_path = os.path.join(os.getcwd(), file_path)

            # Download recording from Twilio
            download_result = twilio_service.download_recording(
                recording_sid, full_path)

            if download_result['success']:
                # Update call record with recording info
                call.twilio_recording_sid = recording_sid
                call.recording_file_path = file_path
                if not call.duration and download_result.get('duration'):
                    call.duration = int(download_result['duration'])
                call.save()

                # Automatically start transcription and summary generation
                self._process_recording_async(call.id)

                response_data = CallSerializer(call).data
                return custom_success_response(response_data)
            else:
                return custom_error_response(
                    message=f"Failed to download recording: {download_result['error']}",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                f"Error downloading recording for call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'], url_path='status')
    def get_call_status(self, request, pk=None):
        try:
            logger.info(f"Getting call status {pk}", extra={
                        "user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            # Get latest status from Twilio if call_sid exists
            if call.twilio_call_sid:
                twilio_service = TwilioService()
                twilio_result = twilio_service.get_call_status(
                    call.twilio_call_sid)

                if twilio_result['success']:
                    call.status = twilio_result['status']
                    if twilio_result.get('duration'):
                        # Convert Twilio's string duration to integer
                        try:
                            call.duration = int(twilio_result['duration'])
                        except (ValueError, TypeError):
                            call.duration = None
                    call.save()

            response_data = CallSerializer(call).data
            return custom_success_response(response_data)
        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting call status {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def _process_recording_async(self, call_id):
        """
        Process recording asynchronously for transcription and summary
        Note: In production, this should be moved to a background task (Celery)
        """
        try:
            call = Call.objects.get(pk=call_id)
            ai_service = AIService()

            # Update transcription status
            call.transcribe_status = 'processing'
            call.save()

            # Transcribe audio
            full_path = os.path.join(os.getcwd(), call.recording_file_path)
            transcription_result = ai_service.transcribe_audio(full_path)

            if transcription_result['success']:
                call.transcribe_content = transcription_result['transcription']
                call.transcribe_status = 'completed'
                call.save()

                # Generate summary
                call.summary_status = 'processing'
                call.save()

                summary_result = ai_service.summarize_transcription(
                    call.transcribe_content)

                if summary_result['success']:
                    call.summary_content = summary_result['summary']
                    call.summary_status = 'completed'
                else:
                    call.summary_status = 'failed'
                call.save()

            else:
                call.transcribe_status = 'failed'
                call.save()

        except Exception as e:
            logger.error(f"Error processing recording async: {str(e)}")

    @action(detail=True, methods=['POST'], url_path='transcribe')
    def transcribe_recording(self, request, pk=None):
        try:
            logger.info(f"Transcribing recording for call {pk}", extra={
                        "user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            if not call.recording_file_path:
                return custom_error_response(
                    message="No recording file found for this call",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Update status to processing
            call.transcribe_status = 'processing'
            call.save()

            ai_service = AIService()
            full_path = os.path.join(os.getcwd(), call.recording_file_path)

            transcription_result = ai_service.transcribe_audio(full_path)

            if transcription_result['success']:
                call.transcribe_content = transcription_result['transcription']
                call.transcribe_status = 'completed'
                call.save()

                response_data = CallSerializer(call).data
                return custom_success_response(response_data)
            else:
                call.transcribe_status = 'failed'
                call.save()
                return custom_error_response(
                    message=f"Transcription failed: {transcription_result['error']}",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                f"Error transcribing recording for call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'], url_path='summarize')
    def summarize_call(self, request, pk=None):
        try:
            logger.info(f"Summarizing call {pk}", extra={"user": request.user})
            call = Call.objects.get(pk=pk, user=request.user)

            if not call.transcribe_content:
                return custom_error_response(
                    message="No transcription available for this call",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Update status to processing
            call.summary_status = 'processing'
            call.save()

            ai_service = AIService()
            summary_result = ai_service.summarize_transcription(
                call.transcribe_content)

            if summary_result['success']:
                call.summary_content = summary_result['summary']
                call.summary_status = 'completed'
                call.save()

                response_data = CallSerializer(call).data
                return custom_success_response(response_data)
            else:
                call.summary_status = 'failed'
                call.save()
                return custom_error_response(
                    message=f"Summary generation failed: {summary_result['error']}",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error summarizing call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'], url_path='audio')
    def serve_audio(self, request, pk=None):
        try:
            logger.info(f"Serving audio for call {pk}", extra={
                        "user_id": request.user.id if request.user.is_authenticated else "anonymous"})

            # Check authentication - allow token in URL parameter for audio playback
            if not request.user.is_authenticated:
                return custom_error_response(
                    message="Authentication required",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            call = Call.objects.get(pk=pk, user=request.user)

            if not call.recording_file_path:
                return custom_error_response(
                    message="No recording file found for this call",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            full_path = os.path.join(os.getcwd(), call.recording_file_path)

            if not os.path.exists(full_path):
                return custom_error_response(
                    message="Recording file not found on server",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # Serve the audio file with proper headers
            response = FileResponse(
                open(full_path, 'rb'),
                content_type='audio/mpeg',
                as_attachment=False
            )
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(full_path)}"'
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET'
            response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
            response['Cache-Control'] = 'no-cache'
            response['Accept-Ranges'] = 'bytes'
            return response

        except Call.DoesNotExist:
            return custom_error_response(
                message="Call not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error serving audio for call {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
