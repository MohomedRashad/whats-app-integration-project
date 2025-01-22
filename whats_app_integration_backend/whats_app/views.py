from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Thread
from .serializers import MessageSerializer, ThreadSerializer, ThreadListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SendMessageView(APIView):
    @swagger_auto_schema(
        operation_summary="Send a Message",
        operation_description="Create a new message. If no thread exists between the sender and receiver, a new thread is created.",
        request_body=MessageSerializer,
        responses={
            201: openapi.Response("Message successfully created", MessageSerializer),
            400: "Bad Request",
        },
    )
    def post(self, request):
        """
        Handle the creation of a new message.
        If no thread exists, a new one is created.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Save the message and return the appropriate response
            message = serializer.save()
            return Response({
                "id": message.id,
                "thread_id": message.thread.id,
                "sender_number": message.thread.sender_number,
                "receiver_number": message.thread.receiver_number,
                "timestamp": message.timestamp,
                "content": message.content,
                "status": message.status,
                "message_type": message.message_type,
            }, status=status.HTTP_201_CREATED)
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

