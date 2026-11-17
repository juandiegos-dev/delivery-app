from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accesos.views import PerfilView, RegistroView

urlpatterns = [
    path("registro/", RegistroView.as_view()),
    path("login/", obtain_auth_token),
    path("yo/", PerfilView.as_view()),
]