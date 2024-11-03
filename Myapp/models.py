from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Case(models.Model):
    """
    Model representing a case, which serves as a container for tasks associated with a specific user.

    Attributes:
    - title (CharField): The title of the case, limited to 150 characters.
    - user (ForeignKey): A foreign key linking the case to a user. When a user is deleted, their cases are also removed.
    - status (CharField): Indicates the current state of the case, with choices of 'OPEN' or 'CLOSED'.

    Inner Classes:
    - StatusChoice (TextChoices): Defines the possible statuses for a case.

    Methods:
    - __str__: Returns a string representation of the case, including the title, associated user, status, and titles of related tasks.
    """

    class StatusChoice(models.TextChoices):
        OPEN = "OPEN", _("Open case")
        CLOSED = "CLOSED", _("Closed case")

    title = models.CharField(max_length=150, verbose_name=_("Case title"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cases")
    status = models.CharField(
        max_length=30,
        choices=StatusChoice.choices,
        default=StatusChoice.OPEN,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def __str__(self):
        """
        Returns a string representation of the case.

        Includes:
        - Title of the case.
        - User associated with the case.
        - Current status of the case.
        - Titles of all tasks related to the case.

        Returns:
            str: A formatted string with case details and associated task titles.
        """
        task_titles = ", ".join([task.title for task in self.tasks.all()])
        return f" {self.title} | {self.user} | {self.status} | {task_titles}"


class Task(models.Model):
    """
    Model representing a task associated with a specific user and case.

    Attributes:
    - user (ForeignKey): The user who created the task.
    - title (CharField): Title of the task, limited to 150 characters.
    - description (TextField): Detailed description of the task, limited to 250 characters.
    - creation_date (DateTimeField): The date and time when the task was created, automatically set upon creation.
    - last_updated_date (DateTimeField): The date and time when the task was last updated, automatically set on each update.
    - completed_date (DateTimeField): The date and time when the task was marked as completed.
    - case (ForeignKey): The case to which this task belongs.
    - status (CharField): Current status of the task, chosen from predefined options.

    Inner Classes:
    - StatusChoice (TextChoices): Defines the possible statuses for a task.

    Methods:
    - save: Custom save method to set the completion date when the task is marked as finished.
    - __str__: Returns a string representation of the task, including related case, title, description, creation date, and status.
    """

    class StatusChoice(models.TextChoices):
        CREATED = "CREATED", _("Created Task")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        FINISHED = "FINISHED", _("Finished Task")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=150, verbose_name=_("Task title"))
    description = models.TextField(max_length=250, verbose_name=_("Task description"))
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(
        max_length=30,
        choices=StatusChoice.choices,
        default=StatusChoice.CREATED,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the completed_date field.

        If the task status changes to 'FINISHED',
        the completed_date is set to the current date and time.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.pk:
            if (
                Task.objects.get(pk=self.pk).status != self.StatusChoice.FINISHED
                and self.status == self.StatusChoice.FINISHED
            ):
                self.completed_date = timezone.now()
        else:
            if self.status == self.StatusChoice.FINISHED:
                self.completed_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the task.

        Includes:
        - Related case title.
        - Task title.
        - Description.
        - Creation date.
        - Status.

        Returns:
            str: A formatted string with the task's case, title, description, creation date, and status.
        """

        return f"{self.case.title} | {self.title} | {self.description} | {self.creation_date} | {self.status}"
