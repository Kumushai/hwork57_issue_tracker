from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from webapp.forms import ProjectForm, SearchForm
from webapp.models import Project


class ProjectListView(ListView):
    template_name = "projects/index.html"
    context_object_name = 'projects'
    model = Project
    ordering = ['-start_date']
    paginate_by = 5
    paginate_orphans = 1

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
        queryset = queryset.exclude(projects__is_deleted=True)
        return queryset


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'projects/create_project.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.groups.filter(name="Project Manager")

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        project.user.add(self.request.user)
        return super().form_valid(form)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.groups.filter(name="Project Manager")


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'projects/delete_project.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return self.request.user.groups.filter(name="Project Manager")


class ProjectDetailView(DetailView):
    template_name = "projects/project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.order_by("-updated_at")
        return context


class ProjectUserView(PermissionRequiredMixin, View):

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        user = self.request.user
        groups = ['Project Manager', 'Team Lead']
        return self.request.user.groups.filter(name__in=groups) and user in project.user.all()

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        all_users = User.objects.all()

        context = {
            'project': project,
            'all_users': all_users
        }

        return render(request, 'projects/projects_users.html', context)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        all_users = User.objects.all()

        if 'add_user' in request.POST:
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(User, pk=user_id)
                project.user.add(user)
                return redirect('webapp:project_user', pk=project.pk)

        elif 'remove_user' in request.POST:
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(User, pk=user_id)
                project.user.remove(user)
                return redirect('webapp:project_user', pk=project.pk)

        context = {
            'project': project,
            'all_users': all_users
        }

        return render(request, 'projects/projects_users.html', context)
