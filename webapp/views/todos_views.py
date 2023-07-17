from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, CreateView

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
        return redirect('project_view', pk=project.pk)


class TodoUpdateView(View):

    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, id=kwargs['pk'])
        form = TodoForm(initial={
            "content": todo.content,
            "details": todo.details,
            "types": todo.types.all(),
            "status": todo.status
        })
        return render(request, "todos/update_todo.html", {"form": form})

    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, id=kwargs['pk'])
        form = TodoForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop("types")
            todo.content = form.cleaned_data.get("content")
            todo.details = form.cleaned_data.get("details")
            todo.status = form.cleaned_data.get("status")
            todo.save()
            todo.types.set(types)
            return redirect("todo_view", pk=todo.pk)
        else:
            return render(request, "todos/update_todo.html", {"form": form})


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


