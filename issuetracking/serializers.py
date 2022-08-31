from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

from issuetracking.models import User,Project,Contributor,Issue,Comment



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


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id','title','description','type','author','date_created','date_updated']
        fields = ['id','title','description','type','date_created','date_updated']
    def create(self,validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)






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