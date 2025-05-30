from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        if not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        return value

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value


class CreateLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'email']

    def validate_phone(self, value):
        if not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        return value

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value
