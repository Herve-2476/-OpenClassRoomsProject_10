from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from issuetracking.models import User,Project



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
