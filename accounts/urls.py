from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', extra_context={'error_message': 'Неверное имя пользователя или пароль.'}), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

]