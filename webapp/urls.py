from django.urls import path

from django.views.generic import RedirectView

from webapp.views.projects_views import ProjectListView
from webapp.views.todos_views import \
    TodoListView, TodoCreateView, TodoDeleteView, TodoDetailView, TodoUpdateView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name="index")),
    path('todos/', ProjectListView.as_view(), name="index"),
    path('todos/add/', TodoCreateView.as_view(), name="todo_add"),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name="todo_view"),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name="update_todo"),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name="delete_todo")
]