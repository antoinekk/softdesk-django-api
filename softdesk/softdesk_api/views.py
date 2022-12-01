from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import AuthorPermission
from .serializers import *
from .models import *

class SignupView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProjectsView(APIView):

    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated & AuthorPermission]

    def get(self, request, id):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, id):
        project = Project.objects.get(id=id)
        self.check_object_permissions(request, project)
        request.data['author'] = project.author.id
        serializer = ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        project = Project.objects.get(id=id)
        self.check_object_permissions(request, project)
        project.delete()
        return Response('Project has been deleted')

class ContributorView(APIView):

    permission_classes = [IsAuthenticated & AuthorPermission]

    def post(self, request, id):
        project = Project.objects.get(id=id)
        self.check_object_permissions(request, project)
        request.data['project'] = project.id
        try:
            Contributor.objects.get(user=request.data['user'], project=project.id)
            return Response('This contributor already exists')
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=request.data['user'])
                serializer = ContributorSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response('This user does not exist')

    def get(self,request, id):
        project = Project.objects.get(id=id)
        contributors = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

class ContributorViewDelete(APIView):

    permission_classes = [IsAuthenticated & AuthorPermission]

    def delete(self, request, project_id, contributor_id):
        project = Project.objects.get(id=project_id)
        self.check_object_permissions(request, project)
        contributor = Contributor.objects.get(user=contributor_id, project=project)
        if contributor.role == 'AUTHOR':
            return Response('Author of the project cannot be deleted')
        else:
            contributor.delete()
            return Response('Contributor has been deleted')

class IssueView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        project = Project.objects.get(id=id)
        request.data['project'] = project.id
        request.data['author'] = request.user.id
        try:
            Contributor.objects.get(id=request.data['assigned_user'], project=project.id)
            serializer = IssueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Contributor.DoesNotExist:
            return Response('You cannot assign this issue because assigned user is not contributing to the project')

    def get(self, request, id):
        project = Project.objects.get(id=id)
        issues = Issue.objects.filter(project=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

class IssueDetailsView(APIView):

    permission_classes = [IsAuthenticated & AuthorPermission]

    def put(self, request, project_id, issue_id):
        project = Project.objects.get(id=project_id)
        issue = Issue.objects.get(id=issue_id)
        self.check_object_permissions(request, issue)
        request.data['project'] = project.id
        request.data['author'] = issue.author.id
        try:
            Contributor.objects.get(id=request.data['assigned_user'], project=project.id)
            serializer = IssueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Contributor.DoesNotExist:
            return Response('You cannot modify this issue because assigned user is not contributing to the project')

    def delete(self, request, project_id, issue_id):
        project = Project.objects.get(id=project_id)
        issue = Issue.objects.get(project=project.id, id=issue_id)
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response('Issue has been deleted')

class CommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, issue_id):
        issue = Issue.objects.get(id=issue_id)
        request.data['issue'] = issue.id
        request.data['author'] = request.user.id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, project_id, issue_id):
        project = Project.objects.get(id=project_id)
        issue = Issue.objects.get(project=project, id=issue_id)
        comments = Comment.objects.filter(issue=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentDetailsView(APIView):

    permission_classes = [IsAuthenticated & AuthorPermission]

    def put(self, request, project_id, issue_id, comment_id):
        issue = Issue.objects.get(id=issue_id)
        comment = Comment.objects.get(id=issue_id)
        self.check_object_permissions(request, comment)
        request.data['issue'] = issue.id
        request.data['author'] = comment.author.id
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, project_id, issue_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, project_id, issue_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response('Comment has been deleted')















