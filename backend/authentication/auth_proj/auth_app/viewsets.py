from .serializers import UserSerializer, SessionSerializer, RoleSerializer, UserRoleSerializer, UserPermissionSerializer
from .models import User, Session, Role, UserRole, UserPermission
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["email"]
    ordering = ["email"]

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = User.objects.get(id=lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer


#
# class MainView(views.APIView):
#     def get(self, request):
#         result = {
#             "/": "This page",
#             "/api/auth_apps/login": "Authorization",
#             "/api/auth_apps/registration": "Registration",
#             "/api/auth_apps/refresh": "Token refresh",
#             "GET: /api/resume/": "List of resumes",
#             "POST: /api/resume/": "New resume",
#             "GET: /api/resume/<int>/": "View resume",
#             "PUT: /api/resume/<int>/": "Update resume",
#             "DELETE: /api/resume/<int>/": "Delete resume",
#         }
#         return Response(result, status=status.HTTP_200_OK)
