import logging
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
import random
import json
from django.conf import settings
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Set up logger
logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def send_message(request):
    try:
        # Simulate receiving a message from the client.
        data = json.loads(request.body)

        # Generate a dynamic timestamp (current time in ISO format)
        timestamp = datetime.utcnow().isoformat()  # Get UTC time in ISO format

        # Available statuses to simulate
        statuses = ['pending', 'sent', 'delivered', 'read', 'failed']
        
        # Randomly select a status for the message
        status = random.choice(statuses)

        # Generate a message ID.
        message_id = str(uuid.uuid4())  # Generate a random message ID (as a mock)

        # Simulate message sending logic
        response = {
            "status": "success",  # This could reflect the actual status returned from the real API
            "message": {
                "message_id": message_id,
                "timestamp": timestamp,
                "status": status  # Randomly chosen status
            }
        }
        logger.info(f"Message sent successfully with ID: {message_id}, Status: {status}")
        return JsonResponse(response, status=200)
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {str(e)}")
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


class TriggerStatusUpdateWebhookView(APIView):
    """
    Simulate the triggering of a status update webhook from WhatsApp.
    This endpoint will call the actual webhook endpoint and log the result.
    """
    def post(self, request):
        # Extract the necessary data from the request (you can also modify this logic to fit your needs)
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
                logging.info(f"Successfully triggered webhook for message_id {message_id} with status {status_update}.")
            else:
                logging.error(f"Failed to trigger webhook. Status Code: {response_from_server.status_code}, Response: {response_from_server.text}")
                server_response = {"error": f"Failed to trigger webhook. Server Response: {response_from_server.text}"}

            # Return a response including both the success message and the server's response
            return Response({
                    "message": "Webhook triggered successfully.",
                    "server_response": response_from_server
                }, status=status.HTTP_200_OK
            )
        except requests.RequestException as e:
            logging.error(f"Error occurred while sending request to webhook: {e}")
            return Response(
                {"error": f"Error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
