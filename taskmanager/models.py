import datetime

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=140)
    created_date = models.DateField(auto_now=True)
    due_date = models.DateField(blank=True, null=True, db_index=True)
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='created_by')
    assignee = models.ForeignKey(
        User, blank=True, null=True, related_name='assignee')
    description = models.TextField()
    priority = models.PositiveIntegerField(default=False)

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-priority"]


class Comment(models.Model):
    author = models.ForeignKey(User)
    task = models.ForeignKey(Task, related_name='comment')
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=False)

    def __str__(self):
        return str(self.task)


class Message(models.Model):
    author = models.ForeignKey(User)
    email_from = models.EmailField()
    email_to = models.EmailField(default=False)
    subject = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField()
