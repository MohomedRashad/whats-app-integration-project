from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID
from django.conf import settings
import requests
from datetime import timedelta, datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Thread, Message
from .serializers import MessageSerializer, ThreadSerializer, ThreadListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SendMessageView(APIView):
    @swagger_auto_schema(
        operation_summary="Send a Message",
        operation_description="Create a new message. If no thread exists between the sender and receiver, a new thread is created.",
        request_body=MessageSerializer,
        responses={201: openapi.Response("Message successfully created", MessageSerializer), 400: "Bad Request"},
    )
    def post(self, request):
        """
        Handle the creation of a new message.
        If no thread exists, a new one is created.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()

            # Get the base URL from settings
            base_url = settings.BASE_URL

            # Construct the mock API URL to simulate sending the message
            mock_send_url = f"{base_url}/whatsapp-mock/send-whatsaap-message/"

            # Simulate calling the WhatsApp mock API to send the message
            response = requests.post(mock_send_url, json={
                "thread_id": message.thread.id,
                "sender_number": message.thread.sender_number,
                "receiver_number": message.thread.receiver_number,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "message_type": message.message_type,
            })

            if response.status_code == 200:
                # Extract message_id from the mock API response
                mock_response = response.json()
                mock_message_id = mock_response.get('message', {}).get('message_id')
                status_from_api = mock_response.get('message', {}).get('status', 'pending')

                if mock_message_id:
                    # Save the message_id from the mock API response
                    message.message_id = mock_message_id
                    message.status = status_from_api  # Use the status returned from the mock API
                    message.save()

                    # If the status is not 'failed', update all messages in the same thread
                    if status_from_api != 'failed':
                        updated_count = Message.objects.filter(thread=message.thread).update(status=status_from_api)
                        print(f"Updated {updated_count} messages to status '{status_from_api}'.")

                    return Response({
                        "message_id": message.message_id,
                        "thread_id": message.thread.id,
                        "sender_number": message.thread.sender_number,
                        "receiver_number": message.thread.receiver_number,
                        "timestamp": message.timestamp,
                        "content": message.content,
                        "status": message.status,
                        "message_type": message.message_type,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "error": "Message ID not returned by the mock API"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({
                    "error": "Failed to send message via mock API"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    """
    Retrieve, update, or delete a specific message.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a message",
        operation_description="Get the details of a message with the given ID.",
        responses={200: MessageSerializer},
    )
    def get(self, request, pk):
        """
        Get the details of a specific message.
        """
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT method to update a message, but only if it's within 1 hour of sending
    @swagger_auto_schema(
        operation_summary="Update a message",
        operation_description="Update the content of a message, only if it was sent within the last hour.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Updated content for the message")
            },
        ),
        responses={200: MessageSerializer, 400: "Bad Request", 403: "Forbidden - Cannot update after 1 hour", 404: "Not Found"},
    )
    def put(self, request, pk):
        """
        Update the content of the message, if the message is within 1 hour of being sent.
        """
        message = get_object_or_404(Message, pk=pk)

        # Check if the message is older than 1 hour
        if timezone.now() - message.timestamp > timedelta(hours=1):
            return Response({"error": "Message cannot be updated after 1 hour."}, status=status.HTTP_403_FORBIDDEN)

        # Update the message content
        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required to update the message."}, status=status.HTTP_400_BAD_REQUEST)

        message.content = content
        message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE method to delete a message, but only if it's within 1 hour of sending
    @swagger_auto_schema(
        operation_summary="Delete a message",
        operation_description="Delete a message, only if it was sent within the last hour.",
        responses={204: "No Content", 403: "Forbidden - Cannot delete after 1 hour", 404: "Not Found"},
    )
    def delete(self, request, pk):
        """
        Delete the message if it's within 1 hour of being sent.
        """
        message = get_object_or_404(Message, pk=pk)

        # Check if the message is older than 1 hour
        if timezone.now() - message.timestamp > timedelta(hours=1):
            return Response({"error": "Message cannot be deleted after 1 hour."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the message
        message.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadListView(APIView):
    @swagger_auto_schema(
        operation_summary="List All Threads",
        operation_description="Retrieve all threads without including messages.",
        responses={
            200: openapi.Response("List of all threads", ThreadSerializer),
        }
    )
    def get(self, request):
        threads = Thread.objects.all()
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadDetailView(APIView):
    """
    Retrieve, update, or delete a specific thread.
    """


    @swagger_auto_schema(
        operation_summary="Retrieve Thread Details",
        operation_description="Retrieve a thread by its ID along with all associated messages.",
        responses={
            200: openapi.Response("Thread details and associated messages", ThreadSerializer),
            404: "Thread not found",
        }
    )
    def get(self, request, pk):
        """
        Retrieve a thread by its ID along with all associated messages.
        """
        thread = get_object_or_404(Thread, pk=pk)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update the read status of a thread",
        operation_description="Set the 'read' status of a thread. Accepts a boolean 'read' field in the request body.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'read': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Set the read status of the thread")
            },
        ),
        responses={200: ThreadSerializer, 400: "Bad Request"},
    )
    def patch(self, request, pk):
        """
        Update the 'read' status of a thread.
        """
        thread = get_object_or_404(Thread, pk=pk)
        
        # Check if 'read' status is provided in the request data
        read_status = request.data.get('read')
        
        if read_status is None:
            return Response({"error": "'read' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the 'read' field
        thread.read = read_status
        thread.save()

        # Return the updated thread details
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a thread and its messages",
        operation_description="Delete the thread with the given ID and all associated messages.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        
        # Delete the thread and its associated messages
        thread.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

#  Webhook views
class WhatsAppNotificationWebhookView(APIView):
    @swagger_auto_schema(
        operation_summary="WhatsApp Notification Webhook",
        operation_description=(
            "Handle notifications from WhatsApp and update the status of messages. "
            "Supports statuses such as 'sent', 'delivered', 'read', and 'failed'."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Unique ID of the message as a UUID.",
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=(
                        "Status of the message. Possible values are 'sent', 'delivered', 'read', and 'failed'."
                    ),
                    enum=["sent", "delivered", "read", "failed"],
                ),
            },
            required=["message_id", "status"],
        ),
        responses={
            200: openapi.Response("Status updated successfully."),
            400: openapi.Response("Invalid request."),
            404: openapi.Response("Message not found."),
        },
    )
    def post(self, request):
        """
        Update the status of a message based on a webhook notification from WhatsApp.
        """
        data = request.data

        # Validate required fields
        message_id = data.get("message_id")
        status_update = data.get("status")

        if not message_id or not status_update:
            return Response(
                {"error": "Both 'message_id' and 'status' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate UUID format for message_id
        try:
            message_id = UUID(message_id)
        except ValueError:
            return Response(
                {"error": "Invalid 'message_id' format. Must be a valid UUID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if status is valid
        valid_statuses = ["sent", "delivered", "read", "failed"]
        if status_update not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of {valid_statuses}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the message and update the status
        try:
            message = Message.objects.get(message_id=message_id)
            message.status = status_update
            message.save()
            return Response(
                {"message": f"Message {message_id} status updated to {status_update}."},
                status=status.HTTP_200_OK,
            )
        except Message.DoesNotExist:
            return Response(
                {"error": f"Message with ID {message_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class WhatsAppIncomingMessageWebhookView(APIView):
    """
    Webhook to handle incoming messages from WhatsApp.
    """
    def post(self, request):
        try:
            # Parse the incoming JSON payload
            payload = request.data

            # Validate required fields
            sender_number = payload.get("sender_number")
            receiver_number = payload.get("receiver_number")
            message_id = payload.get("message_id")
            content = payload.get("content", "")
            timestamp = payload.get("timestamp")
            message_type = payload.get("message_type", "text")

            if not (sender_number and receiver_number and message_id):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if it's a reply to an existing thread
            thread = Thread.objects.filter(
                sender_number=receiver_number,
                receiver_number=sender_number
            ).first()

            if not thread:
                # Create a new thread for a new conversation
                thread = Thread.objects.create(
                    sender_number=receiver_number,
                    receiver_number=sender_number,
                    created_at=datetime.now(),
                    last_accessed_at=datetime.now(),
                    read=False
                )

            # Save the message to the database
            message = Message.objects.create(
                thread=thread,
                timestamp=datetime.fromisoformat(timestamp),
                content=content,
                message_type=message_type
            )

            return Response({
                "message": "Message received and saved.",
                "data": {
                    "id": message.id,
                    "thread_id": thread.id,
                    "content": message.content,
                    "timestamp": message.timestamp
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
