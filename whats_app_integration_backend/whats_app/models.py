from django.db import models
import uuid
from datetime import datetime

class Thread(models.Model):
    sender_number = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=datetime.now)
    last_accessed_at = models.DateTimeField(default=datetime.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Thread between {self.sender_number} and {self.receiver_number}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    timestamp = models.DateTimeField(default=datetime.now)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'PENDING'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed')
    ], default='pending')
    message_type = models.CharField(max_length=20, choices=[ 
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('location', 'Location'),
        ('template', 'Template'),
        ('sticker', 'Sticker'),
        ('video', 'Video'),
        ('interactive', 'Interactive')
    ])
    media_url = models.URLField(blank=True, null=True)
    preview_url = models.BooleanField(default=False)
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_language = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Message from {self.thread.sender_number} to {self.thread.receiver_number} at {self.timestamp}"
