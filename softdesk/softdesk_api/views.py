from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from softdesk_api.permissions import *
from .serializers import *
from .models import *

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProjectsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.data['author'] = request.user.id
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
        return Response(serializer.data)

    def get(self, request):
        projects = Project.objects.filter(contributor__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, id):
        project = Project.objects.get(id=id)
        request.data['author'] = project.author.id
        serializer = ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        project = Project.objects.get(id=id)
        project.delete()
        return Response('Project deleted')


