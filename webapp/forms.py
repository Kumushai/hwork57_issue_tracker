from django import forms
from django.forms import widgets

from webapp.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ["content", "status", "details", "types"]
        widgets = {"details": widgets.Textarea(attrs={"cols": 30, "rows": 7})}
        error_messages = {"title": {"required": "Поле обязательное"}}

