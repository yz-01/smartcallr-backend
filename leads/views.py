from django.shortcuts import render
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from .models import Lead
from .serializers import LeadSerializer, CreateLeadSerializer
from utils.response_template import custom_success_response, custom_error_response

logger = logging.getLogger(__name__)


class LeadViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='list')
    def list_leads(self, request):
        try:
            logger.info("Fetching leads list", extra={"user": request.user})
            leads = Lead.objects.filter(created_by=request.user)
            serializer = LeadSerializer(leads, many=True)
            return custom_success_response(serializer.data)
        except Exception as e:
            logger.error("Error fetching leads list", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['POST'], url_path='create')
    def create_lead(self, request):
        try:
            logger.info("Creating new lead", extra={"user": request.user})
            serializer = CreateLeadSerializer(data=request.data)
            if serializer.is_valid():
                lead = serializer.save(created_by=request.user)
                response_serializer = LeadSerializer(lead)
                return custom_success_response(
                    response_serializer.data,
                    status.HTTP_201_CREATED
                )
            return custom_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error creating lead", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'], url_path='detail')
    def get_lead(self, request, pk=None):
        try:
            logger.info(f"Fetching lead {pk}", extra={"user": request.user})
            lead = Lead.objects.get(pk=pk, created_by=request.user)
            serializer = LeadSerializer(lead)
            return custom_success_response(serializer.data)
        except Lead.DoesNotExist:
            return custom_error_response(
                message="Lead not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error fetching lead {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['PUT'], url_path='update')
    def update_lead(self, request, pk=None):
        try:
            logger.info(f"Updating lead {pk}", extra={"user": request.user})
            lead = Lead.objects.get(pk=pk, created_by=request.user)
            serializer = CreateLeadSerializer(lead, data=request.data)
            if serializer.is_valid():
                updated_lead = serializer.save()
                response_serializer = LeadSerializer(updated_lead)
                return custom_success_response(response_serializer.data)
            return custom_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Lead.DoesNotExist:
            return custom_error_response(
                message="Lead not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating lead {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['DELETE'], url_path='delete')
    def delete_lead(self, request, pk=None):
        try:
            logger.info(f"Deleting lead {pk}", extra={"user": request.user})
            lead = Lead.objects.get(pk=pk, created_by=request.user)
            lead.delete()
            return custom_success_response(
                {"message": "Lead deleted successfully"},
                status.HTTP_204_NO_CONTENT
            )
        except Lead.DoesNotExist:
            return custom_error_response(
                message="Lead not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting lead {pk}", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
