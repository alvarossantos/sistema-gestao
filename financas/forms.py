from typing import cast

from django import forms

from . import models


class ContaForm(forms.ModelForm):
    class Meta:
        model = models.Conta
        fields = ["nome", "tipo", "saldo_inicial", "ativa"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "saldo_inicial": forms.NumberInput(attrs={"class": "form-control"}),
            "ativa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome",
            "tipo": "Tipo",
            "saldo_inicial": "Saldo Inicial",
            "ativa": "Ativa",
        }


class CartaoCreditoForm(forms.ModelForm):
    class Meta:
        model = models.CartaoCredito
        fields = [
            "nome",
            "limite",
            "dia_fechamento",
            "dia_vencimento",
            "conta_pagamento",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "limite": forms.NumberInput(attrs={"class": "form-control"}),
            "dia_fechamento": forms.NumberInput(attrs={"class": "form-control"}),
            "dia_vencimento": forms.NumberInput(attrs={"class": "form-control"}),
            "conta_pagamento": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "nome": "Nome",
            "limite": "Limite",
            "dia_fechamento": "Dia de Fechamento",
            "dia_vencimento": "Dia de Vencimento",
            "conta_pagamento": "Conta de Pagamento",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            field = cast(forms.ModelChoiceField, self.fields["conta_pagamento"])
            field.queryset = models.Conta.objects.filter(usuario=user)

    def clean(self):
        cleaned_data = super().clean()
        for campo in ("dia_fechamento", "dia_vencimento"):
            valor = cleaned_data.get(campo)
            if valor is not None and not (1 <= valor <= 31):
                self.add_error(campo, "Informe um dia entre 1 e 31.")

        return cleaned_data


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = models.Categoria
        fields = ["nome", "tipo", "categoria_pai", "cor", "ativa"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "categoria_pai": forms.Select(attrs={"class": "form-control"}),
            "cor": forms.TextInput(attrs={"class": "form-control"}),
            "ativa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome",
            "tipo": "Tipo",
            "categoria_pai": "Categoria Pai",
            "cor": "Cor",
            "ativa": "Ativa",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            field = cast(forms.ModelChoiceField, self.fields["categoria_pai"])
            field.queryset = models.Categoria.objects.filter(usuario=user)
            if self.instance.pk:
                field.queryset = field.queryset.exclude(pk=self.instance.pk)

    def clean(self):
        cleaned_data = super().clean()
        categoria_pai = cleaned_data.get("categoria_pai")
        tipo = cleaned_data.get("tipo")

        if categoria_pai and tipo:
            if categoria_pai.tipo != tipo:
                self.add_error(
                    "categoria_pai",
                    f"A categoria pai '{categoria_pai.nome}' é do tipo "
                    f"'{categoria_pai.get_tipo_display()}', mas esta categoria é do tipo '{tipo}'. "
                    f"Escolha uma categoria pai do mesmo tipo.",
                )
        return cleaned_data


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = models.CentroCusto
        fields = ["nome", "ativo"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome",
            "ativo": "Ativo",
        }


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = models.FormaPagamento
        fields = ["nome"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "nome": "Nome",
        }
