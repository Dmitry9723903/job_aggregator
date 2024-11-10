from django.urls import path, include
from .views import RegisterView, UserListView, UserDetailView, HomePageView, SessionCreateView, SessionListView, SessionDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('sessions/', SessionListView.as_view(), name='session-list'),
    path('sessions/create/', SessionCreateView.as_view(), name='session-create'),
    path('sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),
]