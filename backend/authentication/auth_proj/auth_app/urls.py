from django.urls import path, include
from .views import CreateUserView

urlpatterns = [
    # ...
    path('api/create-user/', CreateUserView.as_view()),
    # ...
]