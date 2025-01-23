from django.urls import path
from .views import SendMessageAPIView, TriggerStatusUpdateWebhookAPIView

urlpatterns = [
    path('send-whatsaap-message/', SendMessageAPIView.as_view(), name='send_message'),
    path('trigger-status-update-webhook/', TriggerStatusUpdateWebhookAPIView.as_view(), name='trigger-status-update-webhook'),
]
