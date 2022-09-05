from rest_framework.permissions import BasePermission
from .models import Project,Issue,Comment
from django.shortcuts import get_object_or_404


class IsContributor(BasePermission):
    message = 'You must be a contributor of this project.'
    def has_permission(self, request, view):
        # in ProjectViewset the key is 'pk' otherwise 'project_pk'
        if 'project_pk' in view.kwargs:
            id_project=view.kwargs['project_pk']
        else:
            id_project=view.kwargs['pk']

        project =get_object_or_404(Project,id=id_project)
        return request.user in project.contributors.all()

class IsProjectOwner(BasePermission):
    message = 'You must be the author of this project.'
    def has_permission(self, request, view):
        # in ProjectViewset the key is 'pk' otherwise 'project_pk'
        if 'project_pk' in view.kwargs:
            id_project=view.kwargs['project_pk']
        else:
            id_project=view.kwargs['pk']
        project =get_object_or_404(Project,id=id_project)
        return request.user == project.author

class IsIssueOwner(BasePermission):
    message = 'You must be the author of this issue.'
    def has_permission(self, request, view):
        issue =get_object_or_404(Issue,id=view.kwargs['pk'])
        return request.user == issue.author

class IsCommentOwner(BasePermission):
    message = 'You must be the author of this comment.'
    def has_permission(self, request, view):
        comment =get_object_or_404(Comment,id=view.kwargs['pk'])
        return request.user == comment.author