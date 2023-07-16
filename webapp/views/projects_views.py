from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView

from webapp.forms import ProjectForm, SearchForm
from webapp.models import Todo, Project


class ProjectListView(ListView):
    template_name = "index.html"
    context_object_name = 'projects'
    model = Project
    ordering = ['-start_date']
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
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(description__icontains=self.search_value))
        return queryset


class ProjectCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        return render(request, "projects/create_project.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project = Project.objects.create(title=form.cleaned_data.get("title"),
                                       description=form.cleaned_data.get("description"),
                                       start_date=form.cleaned_data.get("start_date"),
                                       end_date=form.cleaned_data.get("end_date"),
                                       )
            return redirect("project_view", pk=project.pk)
        else:
            return render(request, "projects/create_project.html", {"form": form})


class ProjectUpdateView(View):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        form = ProjectForm(initial={
            "title": project.title,
            "description": project.description,
            "start_date": project.start_date,
            "end_date": project.end_date
        })
        return render(request, "projects/update_project.html", {"form": form})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project.title = form.cleaned_data.get("title")
            project.description = form.cleaned_data.get("description")
            project.start_date = form.cleaned_data.get("start_date")
            project.end_date = form.cleaned_data.get('end_date')
            project.save()
            return redirect("project_view", pk=project.pk)
        else:
            return render(request, "projects/update_project.html", {"form": form})


class ProjectDeleteView(View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        return render(request, "projects/delete_project.html", {"project": project})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        project.delete()
        return redirect("index")


class ProjectDetailView(TemplateView):
    template_name = "projects/project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, id=kwargs['pk'])
        return context

