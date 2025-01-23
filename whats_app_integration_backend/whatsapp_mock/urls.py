from django.urls import path
from . import views
from .views import TriggerStatusUpdateWebhookView

urlpatterns = [
    path('send-whatsaap-message/', views.send_message, name='send_message'),
    path('trigger-status-update-webhook/', TriggerStatusUpdateWebhookView.as_view(), name='trigger-status-update-webhook'),
]
