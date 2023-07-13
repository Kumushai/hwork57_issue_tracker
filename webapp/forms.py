from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.html import format_html

from webapp.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ["content", "status", "details", "types", "project"]
        widgets = {"details": widgets.Textarea(attrs={"cols": 30, "rows": 7}),
                   "types": widgets.CheckboxSelectMultiple()}
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




