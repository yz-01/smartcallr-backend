import os
import requests
from twilio.rest import Client
from django.conf import settings
from decouple import config
import logging

logger = logging.getLogger(__name__)


class TwilioService:
    def __init__(self):
        self.account_sid = config('TWILIO_ACCOUNT_SID')
        self.auth_token = config('TWILIO_AUTH_TOKEN')
        self.phone_number = config('TWILIO_PHONE_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)

    def initiate_call(self, to_number, from_number=None):
        """
        Initiate a call using Twilio with recording enabled
        """
        try:
            if not from_number:
                from_number = self.phone_number

            # Create the call with recording enabled
            call = self.client.calls.create(
                to=to_number,
                from_=from_number,
                url=settings.TWILIO_VOICE_URL,
                record=True  # Enable call recording
            )

            logger.info(f"Call initiated with recording: {call.sid}")
            return {
                'success': True,
                'call_sid': call.sid,
                'status': call.status
            }

        except Exception as e:
            logger.error(f"Failed to initiate call: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_call_status(self, call_sid):
        """
        Get the current status of a call
        """
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                'success': True,
                'status': call.status,
                'duration': call.duration
            }
        except Exception as e:
            logger.error(f"Failed to get call status: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def end_call(self, call_sid):
        """
        End an active call
        """
        try:
            call = self.client.calls(call_sid).update(status='completed')
            return {
                'success': True,
                'status': call.status
            }
        except Exception as e:
            logger.error(f"Failed to end call: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_call_recordings(self, call_sid):
        """
        Get recordings for a specific call
        """
        try:
            recordings = self.client.recordings.list(call_sid=call_sid)
            recording_data = []

            for recording in recordings:
                recording_data.append({
                    'sid': recording.sid,
                    'duration': recording.duration,
                    'status': recording.status,
                    'date_created': recording.date_created,
                    'uri': recording.uri
                })

            return {
                'success': True,
                'recordings': recording_data
            }
        except Exception as e:
            logger.error(f"Failed to get recordings: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def download_recording(self, recording_sid, file_path):
        """
        Download recording file from Twilio
        """
        try:
            # Get recording details
            recording = self.client.recordings(recording_sid).fetch()

            # Download the recording
            recording_url = f"https://api.twilio.com{recording.uri.replace('.json', '.mp3')}"

            response = requests.get(recording_url, auth=(
                self.account_sid, self.auth_token))

            if response.status_code == 200:
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                return {
                    'success': True,
                    'file_path': file_path,
                    'duration': recording.duration
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to download: HTTP {response.status_code}"
                }

        except Exception as e:
            logger.error(f"Failed to download recording: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
