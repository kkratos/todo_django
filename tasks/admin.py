from django.contrib import admin
from django.utils import timezone

from . import models


# Register your models here.

def mark_completed(model_admin, request, queryset):
    queryset.update(status=models.TaskStatus.COMPLETED,
                    completed_at=timezone.now())


mark_completed.short_description = 'Mark these task as complete'


def mark_pending(model_admin, request, queryset):
    queryset.update(status=models.TaskStatus.PENDING,
                    completed_at=timezone.now())


mark_pending.short_description = 'Mark these task as pending'


class TaskAdmin(admin.ModelAdmin):
    fields = [
        'content',
        ('deadline', 'tags')
    ]

    list_display = ['content', 'status', 'deadline', 'get_all_tags']  # this allows to render additional attributes
    list_editable = ['status']
    actions = [mark_completed, mark_pending]
    list_filter = ['status', 'deadline', 'tags']
    search_fields = ['content', 'tags__name']
    ordering = ['status']

    def get_ordering(self, request):
        if request.user.is_superuser:
            return['status']
        else:
            return['deadline']


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Tag)
