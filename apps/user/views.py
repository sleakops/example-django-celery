# accounts/views.py
from django.contrib.auth.views import LoginView, LogoutView
from .forms import BootstrapAuthenticationForm  # opcional, ver abajo

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = BootstrapAuthenticationForm  # o AuthenticationForm por defecto
    redirect_authenticated_user = True  # si ya está logueado, redirige

class UserLogoutView(LogoutView):
    next_page = "home"  # a dónde ir después de logout
