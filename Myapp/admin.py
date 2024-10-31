from django.contrib import admin

from .models import Case, Task


class TaskAdmin(admin.ModelAdmin):
    model = Task
    fields = ["case", "title", "description", "user", "status"]
    readonly_fields = ["creation_date", "completed_date"]


class CaseAdmin(admin.ModelAdmin):
    model = Case
    fields = ["title", "user", "status"]


admin.site.register(Case, CaseAdmin)
admin.site.register(Task, TaskAdmin)
