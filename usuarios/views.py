from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms, models


def cadastro_view(request):
    if request.method == "POST":
        form = forms.CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("usuarios:usuario-login")
    else:
        form = forms.CadastroForm()
    return render(request, "usuario_cadastro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("financas:conta-listar")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "usuario_login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("usuarios:usuario-login")


@login_required
def perfil_view(request):
    return render(request, "usuario_perfil.html", {"usuario": request.user})


@login_required
def perfil_atualizar_view(request):
    usuario = models.Usuario.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = forms.PerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("usuarios:usuario-perfil")
    else:
        form = forms.PerfilForm(instance=usuario)
    return render(request, "usuario_perfil_update.html", {"form": form})
