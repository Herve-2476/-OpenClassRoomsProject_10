from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from issuetracking.models import User, Project, Contributor, Issue, Comment, Contributor


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]

    def create(self, data):
        data["password"] = make_password(data["password"])
        return super().create(data)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("Ce champ ne peut être vide")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Ce champ ne peut être vide")
        return value


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "role"]


class ContributorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user"]

    def create(self, data):

        project = Project.objects.filter(id=self.context["view"].kwargs["project_pk"])[
            0
        ]

        if data["user"] not in project.contributors.all():
            data["role"] = "collaborator"
            data["project"] = project
            return super().create(data)
        raise ValidationError(
            detail="The user you want to add is already a collaborator of this project"
        )


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "date_created", "date_updated"]

    def create(self, data):
        data["author"] = self.context["request"].user
        project = super().create(data)
        Contributor.objects.create(
            user=self.context["request"].user, project=project, role="author"
        )

        return project


class ProjectDetailSerializer(serializers.ModelSerializer):

    project_contributors = ContributorSerializer(many=True)

    class Meta:

        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "date_created",
            "date_updated",
            "project_contributors",
            "issues",
        ]


class ProjectIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "author_id",
            "assignee",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        project = Project.objects.filter(id=self.context["view"].kwargs["project_pk"])[
            0
        ]
        if data["assignee"] in project.contributors.all():
            data["author"] = self.context["request"].user
            data["project"] = project
            return super().create(data)
        raise ValidationError(detail="Assignee is not in the list of the contributors")

    def update(self, instance, data):

        project = Project.objects.filter(id=self.context["view"].kwargs["project_pk"])[
            0
        ]
        if data["assignee"] in project.contributors.all():
            return super().update(instance, data)
        raise ValidationError(detail="Assignee is not in the list of the contributors")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "description",
            "author_id",
            "issue_id",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        data["author"] = self.context["request"].user
        data["issue"] = get_object_or_404(
            Issue, id=self.context["view"].kwargs["issue_pk"]
        )
        return super().create(data)
