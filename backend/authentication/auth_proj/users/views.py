from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from .models import User, Session
from auth_proj.helpers import FileLogger
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

logger = logging.getLogger(__name__)


class LoggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = FileLogger

    def request_logger(self, request):
        logger.info(f"{self.__class__.__name__}: {request.method} request received.")

    def log_request(self, request, *args, **kwargs):
        user = request.user
        log_file_name = f"{user}.log"
        self.filelogger = FileLogger(
            settings.FLAG_DIR / log_file_name,
            disabled=False,
        )
        return self.filelogger.append(f"User {request.user.id} accessed the home page", timestamp=True)


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        log_file_name = f"{instance}.log"
        filelogger = FileLogger(
            settings.FLAG_DIR / log_file_name,
            disabled=False,
        )
        filelogger.append(f"User {instance} was created", timestamp=True)


class BaseUserMixin(LoggerMixin):
    queryset = User.objects.all()


class RegisterView(BaseUserMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        self.request_logger(self.request)
        logger.info(f"User {user.id} registered successfully")
        return user

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        response = super().create(request, *args, **kwargs)
        login_url = reverse('token_obtain_pair', request=request)
        home_page = reverse('home', request=request)
        response.data['message'] = "Please log in"
        response.data['links'] = {
            "login": login_url,
            "home page": home_page
        }
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Перенаправление пользователя в его профиль после успешной авторизации
    """
    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            logger.info(f"User {request.user.id} logged in successfully")

        profile_url = reverse('user_profile', request=request)
        custom_response = response.data.copy()
        custom_response['user_profile'] = profile_url
        return Response(custom_response)


class UserProfileView(BaseUserMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.log_request(request)
        logger.info(f"User {request.user.id} accessed their profile")
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)


class LogoutView(BaseUserMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.log_request(request)
        refresh_token = request.COOKIES.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        logger.info(f"User {request.user.id} logged out successfully")
        return Response(status=status.HTTP_205_RESET_CONTENT)


class HomePageView(APIView):
    permission_classes = [AllowAny]  # Allow non-authenticated access

    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"Authenticated User {request.user.id} accessed the home page")
        else:
            logger.debug(f"Anonymous User accessed the home page")

        login_url = reverse('token_obtain_pair', request=request)
        register_url = reverse('register', request=request)
        profile = reverse('user_profile', request=request)
        logout = reverse('logout', request=request)
        response_data = {
            "message": "Welcome to the home page",
            "links": {
                "register": register_url,
                "login": login_url,
                "profile": profile,
                "logout": logout
            }
        }

        return Response(response_data)



"""
На клиентской стороне, после получения токена, возможный вариант перенаправления пользователя в его профиль 
используя URL, который был возвращен в ответе. 
TODO К этому вернуться при осыслении сервиса на реакте.
Пример на JavaScript:
fetch('login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password'
  })
})
.then(response => response.json())
.then(data => {
  if (data.access) {
    // Перенаправление на профильный кабинет
    window.location.href = data.profile_url;
  }
})
.catch(error => console.error(error));
"""


# __________________________________________________________________
# class UserListView(BaseUserMixin, generics.ListAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
# class UserDetailView(BaseUserMixin, generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def update(self, request, *args, **kwargs):
#         self.log_request(request)
#         return super().update(request, *args, **kwargs)

# class BaseSessionMixin(LoggerMixin):
#     queryset = Session.objects.all()

# class SessionCreateView(BaseSessionMixin, generics.CreateAPIView):
#     serializer_class = SessionSerializer
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         self.log_request(request)
#         return super().create(request, *args, **kwargs)
#
#
# class SessionListView(BaseSessionMixin, generics.ListAPIView):
#     serializer_class = SessionSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class SessionDetailView(BaseSessionMixin, generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = SessionSerializer
#     permission_classes = [IsAuthenticated]
#
#     def update(self, request, *args, **kwargs):
#         self.log_request(request)
#         return super().update(request, *args, **kwargs)
#
#
