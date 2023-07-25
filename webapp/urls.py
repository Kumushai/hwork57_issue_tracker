from django.urls import path

from django.views.generic import RedirectView

from webapp.views import TodoCreateView, TodoDetailView, TodoUpdateView, TodoDeleteView
from webapp.views.projects_views import ProjectListView, ProjectCreateView, ProjectDetailView, \
    ProjectDeleteView, ProjectUpdateView, \
    ProjectUserView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="webapp:index")),
    path('projects/', ProjectListView.as_view(), name="index"),
    path('projects/add/', ProjectCreateView.as_view(), name="project_add"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project_view"),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name="update_project"),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name="delete_project"),
    path('project/<int:pk>/todos/add/', TodoCreateView.as_view(), name="project_todo_add"),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name="todo_view"),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name="update_todo"),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name="delete_todo"),
    path('project/<int:pk>/users', ProjectUserView.as_view(), name='project_user'),
]
