from django.urls import path

from django.views.generic import RedirectView

from webapp.views.projects_views import ProjectListView, ProjectCreateView, ProjectDetailView, \
    ProjectDeleteView, ProjectUpdateView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name="index")),
    path('projects/', ProjectListView.as_view(), name="index"),
    path('projects/add/', ProjectCreateView.as_view(), name="project_add"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project_view"),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name="update_project"),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name="delete_project")
]