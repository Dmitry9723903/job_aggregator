from rest_framework import status
from rest_framework import views
from rest_framework.response import Response


class MainView(views.APIView):
    def get(self, request):
        result = {
            "/": "This page",
            "/api/auth/login": "Authorization",
            "/api/auth/registration": "Registration",
            "/api/auth/refresh": "Token refresh",
            "GET: /api/resume/": "List of resumes",
            "POST: /api/resume/": "New resume",
            "GET: /api/resume/<int>/": "View resume",
            "PUT: /api/resume/<int>/": "Update resume",
            "DELETE: /api/resume/<int>/": "Delete resume",
        }
        return Response(result, status=status.HTTP_200_OK)