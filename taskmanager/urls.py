from django.conf.urls import url

from website.taskmanager import views

urlpatterns = [
    url(r'^$', views.tasks_list, name='all_tasks'),
    url(r'^add_task/$', views.add_task, name='task_add'),
    url(r'^mark-done/(?P<task_id>[\w+:-]+)/$',
        views.mark_as_done, name='task_mark_done'),
    url(r'^edit_task/(?P<task_id>[\w+:-]+)/$', views.edit_task, name='task_edit'),
    url(r'^delete_task/(?P<task_id>[\w+:-]+)/$', views.delete_task, name='task_delete'),
    url(r'^edit_task/(?P<task_id>[\w+:-]+)/comments/$',
        views.comment, name='comment'),
    url(r'^edit_task/(?P<task_id>[\w+:-]+)/comments-read/$',
        views.see_comment, name='see_comment')
]
