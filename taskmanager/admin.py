from django.contrib import admin

from website.taskmanager.models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ('assignee', 'created_by', 'name',
                    'completed', 'due_date', 'priority', 'description',)
    raw_id_fields = ('assignee', )
    list_per_page = 50
    ordering = ('priority',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'body', 'task')


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
