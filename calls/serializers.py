from rest_framework import serializers
from .models import Call


class CallSerializer(serializers.ModelSerializer):
    duration_formatted = serializers.ReadOnlyField()
    lead_name = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = [
            'id', 'phone_number', 'twilio_call_sid', 'twilio_recording_sid', 'status',
            'start_time', 'end_time', 'duration', 'duration_formatted',
            'recording_file_path', 'transcribe_status', 'transcribe_content',
            'summary_status', 'summary_content', 'notes', 'created_at', 'updated_at',
            'lead_name'
        ]
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'twilio_call_sid', 'twilio_recording_sid']

    def get_lead_name(self, obj):
        return obj.lead.name if obj.lead else None


class InitiateCallSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    lead_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_phone_number(self, value):
        if not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        return value


class EndCallSerializer(serializers.Serializer):
    call_id = serializers.IntegerField()
    duration = serializers.IntegerField(min_value=0)
    notes = serializers.CharField(required=False, allow_blank=True)


class UploadRecordingSerializer(serializers.Serializer):
    call_id = serializers.IntegerField()
    recording = serializers.FileField()

    def validate_recording(self, value):
        # Validate file extension
        allowed_extensions = ['.wav', '.mp3']
        file_extension = value.name.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError(
                f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
            )

        # Validate file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if value.size > max_size:
            raise serializers.ValidationError(
                "File size too large. Maximum size is 50MB.")

        return value
