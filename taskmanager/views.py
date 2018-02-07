from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
import datetime

from website.taskmanager.forms import EditTaskForm, AddTaskForm, CommentForm
from website.taskmanager.models import Task, Comment, Message


@login_required
def tasks_list(request):
    hide_completed = request.GET.get('hide_completed', False)
    tasks = Task.objects.all()
    button_pushed_filter_due_date = request.GET.get('button_pushed_filter_due_date', False)
    if button_pushed_filter_due_date:
        tasks = tasks.order_by('due_date')
    check_if_any_task_is_overdue(request)
    if hide_completed:
        tasks = tasks.filter(completed=False)

    return TemplateResponse(request, 'tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            new_task = Task(
                assignee=form.cleaned_data.get('assignee'),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                created_by=request.user,
                due_date=form.cleaned_data.get('due_date'),
                priority=form.cleaned_data.get('priority'),
            )
            new_task.save()

            # Send email alert only if Notify checkbox is checked AND assignee is not same as the submitter
            if "notify" in request.POST and new_task.assignee_id != request.user.id:
                send_notify_mail(request, new_task)
            else:
                messages.success(
                    request, "Since the task assignee is you yourself, the email will not be stored in database")
                # new_task

            return HttpResponseRedirect(reverse('all_tasks'))
        else:
            return TemplateResponse(request, 'edit_task.html', {'errors': form.errors})
    else:
        return TemplateResponse(request, 'edit_task.html', {})


@login_required
def mark_as_done(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save(update_fields=['completed'])
    except Task.DoesNotExist:
        raise Http404

    return HttpResponseRedirect(reverse('all_tasks'))


@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        form = EditTaskForm(instance=Task.objects.get(
            id=task_id), data=request.POST)

        if form.is_valid():
            new_task = Task(
                assignee=form.cleaned_data.get('assignee'),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                created_by=request.user,
                due_date=form.cleaned_data.get('due_date'),
                priority=form.cleaned_data.get('priority'),
            )
            new_task.save()


            if "notify" in request.POST and new_task.assignee_id != request.user.id:
                send_notify_mail(request, new_task)
            else:
                messages.success(request, "Since the task assignee is you yourself, the email will not be stored in database")
            return HttpResponseRedirect(reverse('all_tasks'))
        else:
            return TemplateResponse(request, 'edit_task.html', {'errors': form.errors})
    else:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404

        form = EditTaskForm(instance=task)
        return TemplateResponse(request, 'edit_task.html', {'form': form, 'edit_task': True, 'task_id': task_id})


@login_required
def delete_task(request, task_id):
    try:
        Task.objects.get(id=task_id).delete()
    except Task.DoesNotExist:
        raise Http404

    return HttpResponseRedirect(reverse('all_tasks'))


@login_required
def comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user,
                task=task,
                body=form.cleaned_data.get('body'),
                date=form.cleaned_data.get('date'),
            )
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            messages.success(request, "The task has been edited.")
            return redirect('task_edit', task_id=task_id)
    else:
        form = CommentForm()
    return TemplateResponse(request, 'comment.html', {'form': form, 'task_id': task_id})
    # 'task_id': task_id


@login_required
def see_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return TemplateResponse(request, 'see_comment.html', {'task': task, 'task_id': task_id})


@login_required
def send_notify_mail(request, task):
    # Send email
    author = User.objects.get(id=request.user.id)
    if task.overdue_status:
        subject = "The task is overdue"
        body = "Due date for the task '%s' that has been assigned to you by %s %s is over. Please visit the site and finish it asap" % (task.name, author.first_name, author.last_name)
    else:
        subject = "New task on the task manager"
        body = "A new task: '%s'on the list has been assigned to you by %s %s. Please visit the site" % (task.name, author.first_name, author.last_name)

    email_from = author.email
    recipient = task.assignee_id
    email_to = User.objects.get(id=recipient).email

    date = datetime.datetime.now()

    mail = Message(
        author=author,
        email_from=email_from,
        email_to=email_to,
        subject=subject,
        date=date,
        body=body,
    )
    mail.save()


@login_required
def check_if_any_task_is_overdue(request):
    tasks = Task.objects.filter(assignee_id=request.user.id, completed=False)
    if tasks:
        for task in tasks:
            if task.overdue_status:
                send_notify_mail(request, task)
            pass
    pass
