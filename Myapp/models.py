from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Case(models.Model):
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
        task_titles = ", ".join([task.title for task in self.tasks.all()])
        return f" {self.title} | {self.user} | {self.status} | {task_titles}"


class Task(models.Model):
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
        return f"{self.case.title} | {self.title} | {self.description} | {self.creation_date} | {self.status}"
