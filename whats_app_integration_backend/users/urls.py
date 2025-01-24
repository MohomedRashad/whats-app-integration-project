from django.urls import path
from .views import UserListView, UserDetailView, UserStatsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('uuid:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
