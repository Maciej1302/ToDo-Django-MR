from locale import format

from rest_framework import serializers

from .models import Case, Task


class TaskSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    last_updated_date =serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    #completed_date =serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Task
        fields = [
            "case",
            "title",
            "description",
            "status",
            "creation_date",
            "last_updated_date",

        ]


class CaseSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=False)

    class Meta:
        model = Case
        fields = ["title", "status", "user", "tasks"]

