from rest_framework import serializers

from .models import Case, Task


class TaskSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    last_updated_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    completed_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "pk",
            "case",
            "title",
            "description",
            "status",
            "creation_date",
            "last_updated_date",
            "completed_date",
        ]

    def validate_status(self, value):
        if (
            self.instance
            and self.instance.status == Task.StatusChoice.FINISHED
            and value != Task.StatusChoice.FINISHED
        ):
            raise serializers.ValidationError(
                "You cannot change the status of a finished task."
            )
        return value

    def validate_case(self, value):
        if value.status != Case.StatusChoice.OPEN:
            raise serializers.ValidationError("You cannot add task to closed case.")
        return value


class CaseSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=False)

    class Meta:
        model = Case
        fields = ["pk", "title", "status", "user", "tasks"]
