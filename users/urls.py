from django.urls import path

from .apps import UsersConfig
from .views import *

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout_all/", LogoutAllView.as_view(), name="logout_all"),
    path("sign_up/", SignUpView.as_view(), name="sign_up"),
]
