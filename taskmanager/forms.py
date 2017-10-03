from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, Form, DateField, IntegerField

from website.taskmanager.models import Task, Comment


class AddTaskForm(Form):
    assignee = CharField(required=True)
    description = CharField(required=False)
    name = CharField(required=True)
    due_date = DateField(required=True)
    priority = IntegerField(min_value=0, required=True)

    def clean_assignee(self):
        assignee = self.cleaned_data.get('assignee')
        try:
            return User.objects.get(username=assignee)
        except User.DoesNotExist:
            raise ValidationError('Assignee does not exist')


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['assignee', 'description', 'name', 'due_date', 'priority', ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'date', 'body', ]
