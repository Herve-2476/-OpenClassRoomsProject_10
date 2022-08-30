from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from issuetracking.models import User,Project,Contributor,Issue,Comment



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password']

    def create(self,validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','title','description','type','author']

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user','project','role']

class ProjectIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title','description','tag','priority','status','project','author','assignee']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['issue','description','author']