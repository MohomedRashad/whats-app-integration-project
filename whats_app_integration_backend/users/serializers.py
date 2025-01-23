from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'created_date', 'is_active']
        read_only_fields = fields  # Mark all fields as read-only
