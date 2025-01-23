import logging
import requests
import uuid
import random
import json
from django.conf import settings
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Set up logger
logger = logging.getLogger(__name__)


class SendMessageAPIView(APIView):
    """
    Simulate receiving and sending a message, returning a randomly generated status.
    """
    
    @swagger_auto_schema(
        operation_description="Simulates receiving and sending a message with a randomly generated status.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Message sent successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": {
                            "message_id": "123e4567-e89b-12d3-a456-426614174001",
                            "timestamp": "2025-01-23T10:00:00Z",
                            "status": "sent"
                        }
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid JSON provided",
                examples={
                    "application/json": {
                        "error": "Invalid JSON"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Unexpected error occurred",
                examples={
                    "application/json": {
                        "error": "Internal Server Error"
                    }
                }
            )
        }
    )
    def post(self, request):
        """
        Simulate receiving a message from the client, generate a random status, and return a message response.
        """
        try:
            # Simulate receiving a message from the client.
            data = request.data

            # Generate a dynamic timestamp (current time in ISO format)
            timestamp = datetime.utcnow().isoformat()  # Get UTC time in ISO format

            # Available statuses to simulate
            statuses = ['pending', 'sent', 'delivered', 'read', 'failed']
            
            # Randomly select a status for the message
            random_status = random.choice(statuses)

            # Generate a message ID.
            message_id = str(uuid.uuid4())  # Generate a random message ID (as a mock)

            # Simulate message sending logic
            response = {
                "status": "success",  # This could reflect the actual status returned from the real API
                "message": {
                    "message_id": message_id,
                    "timestamp": timestamp,
                    "status": random_status  # Randomly chosen status
                }
            }
            logger.info(f"Message sent successfully with ID: {message_id}, Status: {random_status}")
            return Response(response, status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TriggerStatusUpdateWebhookAPIView(APIView):
    """
    Simulate the triggering of a status update webhook from WhatsApp.
    """
    
    @swagger_auto_schema(
        operation_description="Simulates the triggering of a status update webhook by sending data to an actual webhook endpoint.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message_id': openapi.Schema(type=openapi.TYPE_STRING, description='The unique ID of the message to be updated'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='The new status for the message')
            },
            required=['message_id', 'status']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Webhook triggered successfully",
                examples={
                    "application/json": {
                        "message": "Webhook triggered successfully.",
                        "server_response": {
                            "status": "success",
                            "message_id": "123e4567-e89b-12d3-a456-426614174001",
                            "status": "sent"
                        }
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Missing required fields",
                examples={
                    "application/json": {
                        "error": "Both 'message_id' and 'status' are required."
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Error occurred while sending request to webhook",
                examples={
                    "application/json": {
                        "error": "Error occurred: <error_message>"
                    }
                }
            )
        }
    )
    def post(self, request):
        """
        Simulates triggering a webhook for status update with a message ID and its new status.
        """
        # Extract the necessary data from the request
        message_id = request.data.get("message_id")
        status_update = request.data.get("status")

        if not message_id or not status_update:
            return Response(
                {"error": "Both 'message_id' and 'status' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Webhook URL (the real system's webhook endpoint)
        webhook_url = f"{settings.BASE_URL}/whatsapp-notification-webhook/"

        # Prepare data to send to the webhook
        data = {
            "message_id": message_id,
            "status": status_update
        }

        # Send the POST request to the actual webhook
        try:
            response_from_server = requests.post(webhook_url, json=data)

            # Log the result of the webhook request
            if response_from_server.status_code == 200:
                try:
                    # Try to parse the server response as JSON
                    server_response = response_from_server.json()
                except ValueError:
                    # If the response is not a valid JSON, log the issue
                    logging.error(f"Invalid JSON response from the server: {response_from_server.text}")
                    server_response = {"error": "Invalid JSON response from the server."}
            else:
                logging.error(f"Failed to trigger webhook. Status Code: {response_from_server.status_code}, Response: {response_from_server.text}")
                server_response = {"error": f"Failed to trigger webhook. Server Response: {response_from_server.text}"}

            # Return a response including both the success message and the server's response
            return Response({
                    "message": "Webhook triggered successfully.",
                    "server_response": server_response
                }, status=status.HTTP_200_OK
            )
        except requests.RequestException as e:
            logging.error(f"Error occurred while sending request to webhook: {e}")
            return Response(
                {"error": f"Error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )