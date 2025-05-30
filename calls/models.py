from django.db import models
from django.contrib.auth.models import User
from leads.models import Lead


class Call(models.Model):
    CALL_STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('ringing', 'Ringing'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('no_answer', 'No Answer'),
        ('busy', 'Busy'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='calls')
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name='calls', null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    twilio_call_sid = models.CharField(max_length=100, null=True, blank=True)
    twilio_recording_sid = models.CharField(
        max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=CALL_STATUS_CHOICES, default='initiated')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(
        null=True, blank=True, help_text="Duration in seconds")
    recording_file_path = models.CharField(
        max_length=500, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Call to {self.phone_number} - {self.status}"

    @property
    def duration_formatted(self):
        """Return duration in MM:SS format"""
        if self.duration:
            try:
                # Convert to int in case it's a string from Twilio
                duration_int = int(self.duration)
                minutes = duration_int // 60
                seconds = duration_int % 60
                return f"{minutes:02d}:{seconds:02d}"
            except (ValueError, TypeError):
                return "00:00"
        return "00:00"
