from rest_framework.viewsets import ModelViewSet

from .models import User,Project
from .serializers import UserSerializer,ProjectSerializer


class UserViewset( ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProjectViewset( ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()