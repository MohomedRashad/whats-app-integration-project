import requests
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

def send_message_to_mock_api(message):
    """
    Sends a message to the mock API for simulation.
    Returns the response from the mock API.
    """
    mock_send_url = settings.WHATSAPP_MOCK_API_SEND_MESSAGE
    try:
        response = requests.post(mock_send_url, json={
            "thread_id": message.thread.id,
            "sender_number": message.thread.sender_number,
            "receiver_number": message.thread.receiver_number,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "message_type": message.message_type,
        }, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        return response
    except requests.Timeout:
        logger.error("Timeout while sending message to mock API.")
        return None
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
