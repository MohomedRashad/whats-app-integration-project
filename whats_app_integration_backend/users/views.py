from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
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