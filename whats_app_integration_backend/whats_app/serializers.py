from rest_framework import serializers
from .models import Message, Thread

class MessageSerializer(serializers.ModelSerializer):
    # Adding sender_number and receiver_number to allow them to be sent in the request for creation
    sender_number = serializers.CharField(write_only=True)
    receiver_number = serializers.CharField(write_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender_number', 'receiver_number', 'content', 'message_type', 'timestamp', 'status', 'message_id']
        read_only_fields = ['message_id', 'status', 'timestamp']
        
    def create(self, validated_data):
        # Extract sender_number and receiver_number from validated data
        sender_number = validated_data.pop('sender_number')
        receiver_number = validated_data.pop('receiver_number')
        
        # Find or create the thread
        thread, created = Thread.objects.get_or_create(
            sender_number=sender_number,
            receiver_number=receiver_number,
            defaults={'read': True}  # Default read state for a new thread
        )

        # Create the message
        message = Message.objects.create(thread=thread, **validated_data)

        # Update the thread's last_accessed_at timestamp
        thread.last_accessed_at = message.timestamp
        thread.save()
        return message

class ThreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'sender_number', 'receiver_number', 'created_at', 'last_accessed_at', 'read']

class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'sender_number', 'receiver_number', 'created_at', 'last_accessed_at', 'read', 'messages']

