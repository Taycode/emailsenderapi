from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    EmailObjectCreate,
    SendEmail
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('email/create/', EmailObjectCreate.as_view()),
    path('email/<int:pk>/send/', SendEmail.as_view())
]
