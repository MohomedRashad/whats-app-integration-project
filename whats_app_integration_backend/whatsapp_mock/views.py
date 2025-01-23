import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
import random
import json
from datetime import datetime

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


@require_POST
@csrf_exempt
def status_update(request):
    pass
