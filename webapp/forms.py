from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.html import format_html

from webapp.models import Todo, Project


class TodoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Todo
        fields = ["content", "status", "details", "types", "project"]
        widgets = {"details": widgets.Textarea(attrs={"cols": 30, "rows": 7}),
                   "types": widgets.CheckboxSelectMultiple}
        error_messages = {"title": {"required": "Поле обязательное"}}

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 4:
            error_message = format_html('<span style="color: red;">Content is too short!</span>')
            raise ValidationError(error_message)
        return content

    def clean_details(self):
        details = self.cleaned_data['details']
        if 'impossible' in details:
            error_message = format_html(
                '<span style="color: red;">Люди ракеты в космос запускают, '
                'а ты код исправить не можешь?! Убери слово "impossible"</span>')
            raise ValidationError(error_message)
        return details


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {'description': widgets.Textarea(attrs={'cols': 30, 'rows': 5}),
                   'start_date': forms.DateInput(attrs={'type': 'date'}),
                   'end_date': forms.DateInput(attrs={'type': 'date'}),
                   }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')

