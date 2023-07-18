from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView

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
        return redirect('todo_view', pk=todo.pk)


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todos/update_todo.html'
    form_class = TodoForm
    context_object_name = 'todo'

    def get_success_url(self):
        return reverse('todo_view', kwargs={'pk': self.object.pk})


class TodoDeleteView(View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, id=kwargs['pk'])
        return render(request, "todos/delete_todo.html", {"todo": todo})

    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, id=kwargs['pk'])
        todo.delete()
        return redirect("index")


class TodoDetailView(DetailView):
    template_name = "todos/todo.html"
    model = Todo


