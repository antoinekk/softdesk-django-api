from rest_framework import permissions
from .models import *

class ProjectPermissions(permissions.BasePermission):
	pass

class ContributorPermissions(permissions.BasePermission):
	pass

class IssuePermissions(permissions.BasePermission):
	pass

class CommentPermissions(permissions.BasePermission):
	pass

