from django.db import models
from django.utils import timezone


class Thread(models.Model):
    sender_number = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    last_accessed_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Thread between {self.sender_number} and {self.receiver_number}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    message_id = models.UUIDField(default=None, null=True, unique=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)
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
        ('image', 'Image')
    ])

    def __str__(self):
        return f"Message from {self.thread.sender_number} to {self.thread.receiver_number} at {self.timestamp}"
