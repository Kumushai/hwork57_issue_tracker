from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView

from webapp.forms import TodoForm, SearchForm
from webapp.models import Todo


class TodoListView(ListView):
    template_name = "index.html"
    context_object_name = 'todos'
    model = Todo
    ordering = ['-created_at']
    paginate_by = 5
    # paginate_orphans = 1

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(content__icontains=self.search_value) |
                                       Q(details__icontains=self.search_value))
        return queryset


class TodoCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TodoForm()
        return render(request, "todos/create_todo.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop("types")
            todo = Todo.objects.create(content=form.cleaned_data.get("content"),
                                       details=form.cleaned_data.get("details"),
                                       status=form.cleaned_data.get("status")
                                       )
            todo.types.set(types)
            return redirect("todo_view", pk=todo.pk)
        else:
            return render(request, "todos/create_todo.html", {"form": form})


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


class TodoDetailView(TemplateView):
    template_name = "todos/todo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo"] = get_object_or_404(Todo, id=kwargs['pk'])
        return context

