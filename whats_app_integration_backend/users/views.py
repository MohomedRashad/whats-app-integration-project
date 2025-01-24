from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .services import get_user_phone_number
from whats_app.models import Thread, Message
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserListView(APIView):
    """
    Retrieve a list of all users.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    Retrieve details of a specific user by ID.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific user by ID.",
        responses={200: UserSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_PATH, description="The ID of the user to retrieve", type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserStatsView(APIView):
    """
    Retrieve statistics about the current user (number of messages sent, number of threads created).
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve statistics for the current user.",
        responses={200: openapi.Response(
            description="Statistics about the user",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'threads_created': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'messages_sent': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )}
    )
    def get(self, request):
        phone_number = get_user_phone_number(request)

        # Count the number of threads created by the user (sender_number matches the user's phone number)
        threads_created = Thread.objects.filter(sender_number=phone_number).count()

        # Count the number of messages sent by the user (sender_number matches the user's phone number)
        messages_sent = Message.objects.filter(thread__sender_number=phone_number).count()

        stats = {
            'threads_created': threads_created,
            'messages_sent': messages_sent
        }

        return Response(stats, status=status.HTTP_200_OK)

