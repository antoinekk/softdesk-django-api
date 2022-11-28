from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from softdesk_api.permissions import check_credentials, check_session
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer
from .models import User, Contributor, Project
import json
import jwt, datetime

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        check_credentials(self, user, password)
        payload = {
            'id': user.id,
            'expiration_date': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30)),
            'creation_date': str(datetime.datetime.utcnow())
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }
        return response

# Here create LogoutView

class ProjectsView(APIView):
    def post(self, request):
        payload = check_session(self, request)
        user = User.objects.filter(id=payload['id']).first()
        request.data['author'] = user.id
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        Contributor.objects.create(user=user, project=project, role='AUTHOR')
        return Response(serializer.data)

    def get(self, request):
        payload = check_session(self, request)
        user = User.objects.filter(id=payload['id']).first()
        projects = Project.objects.filter(contributor__user=user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
