from django.urls import path

from webapp.views import todo_list_view

urlpatterns = [
    path('', todo_list_view, name='index'),
]

