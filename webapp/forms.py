from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ["content", "status", "details", "types"]
        widgets = {"details": widgets.Textarea(attrs={"cols": 30, "rows": 7}),
                   "types": widgets.CheckboxSelectMultiple()}
        error_messages = {"title": {"required": "Поле обязательное"}}

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 4:
            raise ValidationError('Content is too short!')
        return content

    def clean_details(self):
        details = self.cleaned_data['details']
        if 'impossible' in details:
            raise ValidationError('Люди ракеты в космос запускают, а ты код исправить не можешь?!')
        return details
