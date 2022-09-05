from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsContributor,IsProjectOwner,IsIssueOwner,IsCommentOwner
from django.shortcuts import get_object_or_404


from .models import User,Project,Contributor,Issue,Comment
from .serializers import ProjectListSerializer,ProjectDetailSerializer
from .serializers import ProjectIssueSerializer,CommentSerializer
from .serializers import UserSignupSerializer
from .serializers import ContributorSerializer,ContributorCreateSerializer

class UserSignupViewset( ModelViewSet):

    http_method_names = ['post']
    serializer_class = UserSignupSerializer
    
 
   

class ProjectViewset( ModelViewSet):

    http_method_names = ['post','get','put','delete']
    serializer_class = ProjectListSerializer 
    permission_classes=[IsAuthenticated]
    
    
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

    http_method_names = ['post','get','delete']
    serializer_class = ContributorSerializer
    create_serializer_class=ContributorCreateSerializer

    permission_classes=[IsAuthenticated,IsContributor]
    owner_permission_classes=[IsAuthenticated(),IsProjectOwner()]
    
    
    def get_queryset(self):

        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    
    def get_serializer_class(self):
        if self.action=="create":
            return self.create_serializer_class
        return super().get_serializer_class()
    
    
    def get_permissions(self):
        if self.action != 'list':
            return self.owner_permission_classes
        return super().get_permissions()

    def destroy(self,request,*args,**kwargs):
        contributor=get_object_or_404(Contributor,user=self.kwargs['pk'])
        self.kwargs['pk']=contributor.id
        return super().destroy(self,request,*args,**kwargs)
 

class ProjectIssueViewset( ModelViewSet):

    http_method_names = ['post','get','put','delete']
    serializer_class = ProjectIssueSerializer
    permission_classes=[IsAuthenticated,IsContributor]    
    owner_permission_classes=[IsAuthenticated(),IsIssueOwner()]


    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def get_permissions(self):
        if self.action in ['update','destroy']:
            return self.owner_permission_classes
        return super().get_permissions()
   
 

class CommentViewset( ModelViewSet):

    http_method_names = ['post','get','put','delete']
    serializer_class = CommentSerializer
    permission_classes=[IsAuthenticated,IsContributor]
    owner_permission_classes=[IsAuthenticated(),IsCommentOwner()]
    
    def get_queryset(self):
        
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def get_permissions(self):
        if self.action in ['update','destroy']:
            return self.owner_permission_classes
        return super().get_permissions()    