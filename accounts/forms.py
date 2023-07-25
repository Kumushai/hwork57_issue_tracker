from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name and not last_name:
            raise forms.ValidationError("Хотя бы одно из полей 'имя' или 'фамилия' должно быть заполнено.")

        return cleaned_data
