from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastro_view, name="usuario-cadastro"),
    path("login/", views.login_view, name="usuario-login"),
    path("logout/", views.logout_view, name="usuario-logout"),
    path("perfil/", views.perfil_view, name="usuario-perfil"),
    path("perfil/atualizar/", views.perfil_atualizar_view, name="usuario-perfil-atualizar"),
]
