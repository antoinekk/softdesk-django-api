from django.urls import path
from .views import SignupView, LoginView, ProjectsView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('projects', ProjectsView.as_view())
]
