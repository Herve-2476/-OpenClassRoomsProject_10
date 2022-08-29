from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    
    email=models.EmailField(max_length=255)

    

class Contributor(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="users")
    project=models.ForeignKey("Project",on_delete=models.CASCADE,related_name="projects")
    role=models.CharField(max_length=16,choices=[("author","Auteur"),("contributor","Contributeur")])

class Project(models.Model):
    choices=[("backend","Back-end"),("frontend","Front-end"),("ios","IOS"),("android","Android")]
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=1024)
    type=models.CharField(max_length=16,choices=choices)
    contributors=models.ManyToManyField(settings.AUTH_USER_MODEL,through="Contributor",related_name="contributors")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="project_author")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



class Issue(models.Model):
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=1024)
    tag=models.CharField(max_length=16,choices=([("bug","Bug"),("task","Tâche"),("improvement","Amélioration")]))
    priority=models.CharField(max_length=16,choices=([("low","Faible"),("normal","moyenne"),("high","Elevée")]))
    status=models.CharField(max_length=16,choices=([("to_do","A faire"),("in_progress","En cours"),("completed","Terminé")]))
    project=models.ForeignKey("Project",on_delete=models.CASCADE,related_name="project")    
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="issue_author")
    assignee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="issue_assignee")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    issue=models.ForeignKey("Issue",on_delete=models.CASCADE,related_name="issue")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comment_author")
    description=models.CharField(max_length=1024)    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
