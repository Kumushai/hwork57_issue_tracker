from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import TodoForm
from webapp.models import Todo, Project


class TodoCreateView(CreateView):
    template_name = 'todos/create_todo.html'
    form_class = TodoForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        todo = form.save(commit=False)
        todo.project = project
        todo.save()
        form.save_m2m()
        return redirect('webapp:todo_view', pk=todo.pk)


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todos/update_todo.html'
    form_class = TodoForm
    context_object_name = 'todo'

    def get_success_url(self):
        return reverse('webapp:todo_view', kwargs={'pk': self.object.pk})


class TodoDeleteView(DeleteView):
    template_name = 'todos/delete_todo.html'
    model = Todo
    context_object_name = 'todo'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})

    def delete(self, request, *args, **kwargs):
        self.object = super().get_object(queryset=None)
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TodoDetailView(DetailView):
    template_name = "todos/todo.html"
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.is_deleted:
            raise Http404("Задача не найдена")
        return obj

