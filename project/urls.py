from rest_framework import routers


from django.contrib import admin
from django.urls import path,include

from issuetracking.views import UserViewset,ProjectViewset

router = routers.SimpleRouter()
router.register('user', UserViewset, basename='user')
router.register('projects', ProjectViewset, basename='projects')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls))
]
