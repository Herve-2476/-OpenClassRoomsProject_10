from rest_framework.permissions import BasePermission
from .models import Project,Contributor,Issue
from django.shortcuts import get_object_or_404


class IsContributor(BasePermission):
    message = 'You must be a contributor of this project.'
    def has_permission(self, request, view):
        project =get_object_or_404(Project,id=view.kwargs['project_pk'])
        return request.user in project.contributors.all()

class IsProjectOwner(BasePermission):
    message = 'You must be the author of this project.'
    def has_permission(self, request, view):
        project =get_object_or_404(Project,id=view.kwargs['project_pk'])
        return request.user == project.author

class IsIssueOwner(BasePermission):
    message = 'You must be the author of this issue.'
    def has_permission(self, request, view):
        issue =get_object_or_404(Issue,id=view.kwargs['pk'])
        return request.user == issue.author


    #def has_object_permission(self, request, view, obj):
        #return obj.user == request.user