from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    path("perfil/atualizar/", views.perfil_atualizar_view, name="perfil_atualizar"),
]
