from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from django.contrib import admin
from django.urls import path,include

from issuetracking.views import ProjectViewset,ProjectUserViewset
from issuetracking.views import ProjectIssueViewset,CommentViewset 
from issuetracking.views import UserSignupViewset

router = routers.SimpleRouter()
router.register('signup', UserSignupViewset, basename='user_signup')

router.register('projects', ProjectViewset, basename='projects')

project_router=routers.NestedSimpleRouter(router,'projects',lookup='project')
project_router.register('users', ProjectUserViewset, basename='projects_users')
project_router.register('issues', ProjectIssueViewset, basename='projects_issues')

issue_router=routers.NestedSimpleRouter(project_router,'issues',lookup='issue')
issue_router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('',include(router.urls)),
    path('',include(project_router.urls)),
    path('',include(issue_router.urls)),
]
