from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from .models import User,Project,Contributor,Issue,Comment
from .serializers import ProjectListSerializer,ProjectDetailSerializer,ContributorSerializer
from .serializers import ProjectIssueSerializer,CommentSerializer
from .serializers import UserSignupSerializer

class UserSignupViewset( ModelViewSet):
    
    serializer_class = UserSignupSerializer
    http_method_names = ['post']
 
   

class ProjectViewset( ModelViewSet):

    serializer_class = ProjectListSerializer    

    permission_classes=[IsAuthenticated]
    http_method_names = ['post','get','put','delete']
    
    def get_queryset(self):
        if self.action=="retrieve":
            project_id=self.kwargs['pk']
            return Project.objects.filter(author=self.request.user,id=project_id)        
        return Project.objects.filter(author=self.request.user)       
    
    
    def destroy(self,request,*args,**kwargs):
        project_id=self.kwargs['pk']
        get_object_or_404(Project, author=self.request.user,id=project_id)
        return super().destroy(self,request,*args,**kwargs)        


    def get_serializer_class(self):
        if self.action in ["retrieve","destroy"]:
            return ProjectDetailSerializer
        return super().get_serializer_class()  


class ProjectUserViewset( ModelViewSet):

    serializer_class = ContributorSerializer

    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

class ProjectIssueViewset( ModelViewSet):

    serializer_class = ProjectIssueSerializer

    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

class CommentViewset( ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        
        return Comment.objects.filter(issue__project=self.kwargs['project_pk'],issue=self.kwargs['issue_pk'])
        