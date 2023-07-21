from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data['error_message'] = 'Неверное имя пользователя или пароль.'
        return response

