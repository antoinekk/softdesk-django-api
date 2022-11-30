from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('projects', ProjectsView.as_view()),
    path('projects/<int:id>/', ProjectDetailsView.as_view()),
    path('projects/<int:id>/users/', ContributorView.as_view()),
    path('projects/<int:project_id>/users/<int:contributor_id>/', ContributorViewDelete.as_view()),
    path('projects/<int:id>/issues/', IssueView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssueDetailsView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', CommentDetailsView.as_view())
]
