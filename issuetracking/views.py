from rest_framework.viewsets import ModelViewSet

from .models import User,Project,Contributor,Issue,Comment
from .serializers import UserSerializer,ProjectSerializer,ProjectUserSerializer
from .serializers import ProjectIssueSerializer,CommentSerializer

class UserViewset( ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProjectViewset( ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectUserViewset( ModelViewSet):

    serializer_class = ProjectUserSerializer
    
    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

class ProjectIssueViewset( ModelViewSet):

    serializer_class = ProjectIssueSerializer
    
    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

class CommentViewset( ModelViewSet):

    serializer_class = CommentSerializer
    
    def get_queryset(self):
        
        return Comment.objects.filter(issue__project=self.kwargs['project_pk'],issue=self.kwargs['issue_pk'])
        