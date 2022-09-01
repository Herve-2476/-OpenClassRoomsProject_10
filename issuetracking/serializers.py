from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

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