from ctypes.wintypes import HHOOK
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from issuetracking.models import User,Project,Contributor,Issue,Comment,Contributor



class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password']

    def create(self,validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)    

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_first_name(self,value):
        if not value:
            raise serializers.ValidationError('Ce champ ne peut être vide')
        return value

    def validate_last_name(self,value):
        if not value:
            raise serializers.ValidationError('Ce champ ne peut être vide')
        return value

class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields =['id','user','project','role']

class ContributorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields =["user"]

    def create(self,validate_data):
        
        project=Project.objects.filter(id=self.context["view"].kwargs["project_pk"])[0]
        print (validate_data,project.contributors.all())
        if validate_data["user"] not in project.contributors.all():
            validate_data["role"]="collaborator"
            validate_data["project"] = project
            return super().create(validate_data)
        print ("gagné")
        raise ValidationError()

    def destroy(self,validate_data):
        print("OK destroy",validate_data)



class ProjectListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project        
        fields = ['id','title','description','type','date_created','date_updated']
    def create(self,validated_data):
        validated_data["author"] = self.context["request"].user #à supprimer
        project=super().create(validated_data)
        Contributor.objects.create(user=self.context["request"].user,project=project,role="author")
        
        return project


class ProjectDetailSerializer(serializers.ModelSerializer):

    project_contributors=ContributorSerializer(many=True)    

    class Meta:
        
        model = Project        
        fields = ['id','title','description','type','date_created','date_updated','project_contributors','issue']
    




class ProjectIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title','description','tag','priority','status','project','author','assignee']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['issue','description','author']