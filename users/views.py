from django.shortcuts import render
import json
import logging

from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from utils.response_template import custom_error_response, custom_success_response

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['POST'], url_path='register', permission_classes=[AllowAny])
    def register_user(self, request):
        try:
            logger.info("User registration attempt",
                        extra={"data": request.data})

            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                user_data = UserSerializer(user).data

                data = {
                    "user": user_data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": "User registered successfully"
                }

                logger.info(f"User registered successfully: {user.username}")
                return custom_success_response(data, status.HTTP_201_CREATED)
            else:
                logger.warning(
                    f"User registration validation failed: {serializer.errors}")
                return custom_error_response(
                    message=str(serializer.errors),
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error("Error during user registration", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['POST'], url_path='login', permission_classes=[AllowAny])
    def login_user(self, request):
        try:
            logger.info("User login attempt", extra={
                        "username": request.data.get('username')})

            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                user_data = UserSerializer(user).data

                data = {
                    "user": user_data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": "Login successful"
                }

                logger.info(f"User logged in successfully: {user.username}")
                return custom_success_response(data)
            else:
                logger.warning(
                    f"User login validation failed: {serializer.errors}")
                return custom_error_response(
                    message=str(serializer.errors),
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error("Error during user login", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['GET'], url_path='profile', permission_classes=[IsAuthenticated])
    def get_user_profile(self, request):
        try:
            logger.info("Retrieving user profile",
                        extra={"user": request.user})

            user_data = UserSerializer(request.user).data

            data = {
                "user": user_data
            }

            return custom_success_response(data)
        except Exception as e:
            logger.error("Error retrieving user profile", exc_info=True)
            return custom_error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
