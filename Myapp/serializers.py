from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Case, Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Fields:
    - pk: Primary key of the task.
    - case: Related case for the task.
    - title: Title of the task.
    - description: Detailed description of the task.
    - status: Current status of the task.
    - creation_date: Date when the task was created (read-only).
    - last_updated_date: Date when the task was last updated (read-only).
    - completed_date: Date when the task was completed (optional, read-only).

    Methods:
    - validate_status: Ensures that the status cannot be changed if the task is marked as finished.
    - validate_case: Ensures that a task cannot be added to a closed case.
    """

    creation_date = serializers.DateTimeField(read_only=True)
    last_updated_date = serializers.DateTimeField(read_only=True)
    completed_date = serializers.DateTimeField(required=False, read_only=True)

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
        """
        Validates the status field.

        Prevents changing the status of a task if it has already been marked as finished.

        Args:
            value: The new status value being assigned to the task.

        Returns:
            The validated status value.

        Raises:
            serializers.ValidationError: If attempting to change the status of a finished task.
        """
        if (
            self.instance
            and self.instance.status == Task.StatusChoice.FINISHED
            and value != Task.StatusChoice.FINISHED
        ):
            raise serializers.ValidationError(
                _("You cannot change the status of a finished task.")
            )
        return value

    def validate_case(self, value):
        """
        Validates the case field.

        Ensures that a task can only be added to an open case.

        Args:
            value: The case instance associated with the task.

        Returns:
            The validated case instance.

        Raises:
            serializers.ValidationError: If attempting to add a task to a closed case.
        """
        if value.status != Case.StatusChoice.OPEN:
            raise serializers.ValidationError(_("You cannot add task to closed case."))
        return value


class CaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Case model.

    Fields:
    - pk: Primary key of the case.
    - title: Title of the case.
    - status: Current status of the case.
    - tasks: List of associated tasks for the case (read-only).
    """

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ["pk", "title", "status", "tasks"]
        read_only_fields = ["user"]
