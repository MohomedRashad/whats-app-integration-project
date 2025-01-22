from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.SendMessageView.as_view(), name='send_message'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('threads/', views.ThreadListView.as_view(), name='thread_list'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
]
