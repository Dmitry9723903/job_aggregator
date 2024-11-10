from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer, SessionSerializer
from .models import User, Session
from auth_proj.helpers import FileLogger
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class LoggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = FileLogger

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


class BaseSessionMixin(LoggerMixin):
    queryset = Session.objects.all()


class RegisterView(BaseUserMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        return super().create(request, *args, **kwargs)


class UserListView(BaseUserMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(BaseUserMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        self.log_request(request)
        return super().update(request, *args, **kwargs)


class SessionCreateView(BaseSessionMixin, generics.CreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        return super().create(request, *args, **kwargs)


class SessionListView(BaseSessionMixin, generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]


class SessionDetailView(BaseSessionMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        self.log_request(request)
        return super().update(request, *args, **kwargs)


class HomePageView(APIView):
    permission_classes = [AllowAny]  # Allow non-authenticated access

    def get(self, request):
        if request.user.is_authenticated:
            log_file_name = f"{request.user.id}.log"
            filelogger = FileLogger(
                settings.FLAG_DIR / log_file_name,
                disabled=False,
            )
            filelogger.append(f"User {request.user.id} accessed the home page", timestamp=True)

        login_url = reverse('token_obtain_pair', request=request)
        register_url = reverse('register', request=request)
        response_data = {
            "message": "Welcome to the home page",
            "links": {
                "login": login_url,
                "register": register_url
            }
        }

        return Response(response_data)






