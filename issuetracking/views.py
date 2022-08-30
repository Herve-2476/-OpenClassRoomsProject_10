from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import User,Project,Contributor,Issue,Comment
from .serializers import ProjectSerializer,ProjectUserSerializer
from .serializers import ProjectIssueSerializer,CommentSerializer
from .serializers import UserSignupSerializer,UserLoginSerializer

class UserSignupViewset( ModelViewSet):
    
    serializer_class = UserSignupSerializer
    def get_queryset(self):
        return None

class UserLoginViewset( ModelViewSet):
    
    serializer_class = UserLoginSerializer
    def get_queryset(self):
        return None




class ProjectViewset( ModelViewSet):

    serializer_class = ProjectSerializer    

    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(author=request.user)


class ProjectUserViewset( ModelViewSet):

    serializer_class = ProjectUserSerializer

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
        