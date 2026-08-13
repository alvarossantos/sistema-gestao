from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

import re

from . import models


class CadastroForm(forms.ModelForm):
    # Campo para confirmar a senha, comparando com o password_hash
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirmar Senha",
    )

    class Meta:
        model = models.Usuario
        fields = [
            "username",
            "primeiro_nome",
            "ultimo_nome",
            "email",
            "password_hash",
        ]
        widgets = {
            # Campos do formulário, form-control para estilização
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "primeiro_nome": forms.TextInput(attrs={"class": "form-control"}),
            "ultimo_nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password_hash": forms.PasswordInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Usuário",
            "primeiro_nome": "Primeiro Nome",
            "ultimo_nome": "Último Nome",
            "email": "Email",
            "password_hash": "Senha",
            "confirmar_senha": "Confirmar Senha",
        }

    # Validação personalizada para confirmar a senha, se as senhas não coincidem, adiciona um erro e limpa os campos
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password_hash")
        confirmar = cleaned_data.get("confirmar_senha")
        if senha and confirmar and senha != confirmar:
            self.add_error("confirmar_senha", "As senhas não coincidem.")
        return cleaned_data

    def clean_password_hash(self):
        senha = self.cleaned_data.get("password_hash")
        if not senha:
            return senha
        erros = []
        if len(senha) < 8:
            erros.append("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", senha):
            erros.append("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", senha):
            erros.append("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"\d", senha):
            erros.append("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_=+\[\]\\;'/`~]", senha):
            erros.append("A senha deve conter pelo menos um caractere especial (!@#$%...).")
        if erros:
            raise ValidationError(" ".join(erros))
        return senha

    # Salva o usuário, criptografando a senha e definindo os campos de superusuário, staff e ativo
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Criptografar a senha antes de salvar com make_password
        instance.password_hash = make_password(self.cleaned_data["password_hash"])
        # Definir os campos de superusuário, staff e ativo
        instance.is_superuser = False
        instance.is_staff = False
        instance.ativo = True
        if commit:
            instance.save()
        return instance


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Usuario
        fields = ["username", "primeiro_nome", "ultimo_nome", "email", "foto"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "primeiro_nome": forms.TextInput(attrs={"class": "form-control"}),
            "ultimo_nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "foto": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Usuário",
            "primeiro_nome": "Primeiro Nome",
            "ultimo_nome": "Último Nome",
            "email": "Email",
            "foto": "Foto",
        }
