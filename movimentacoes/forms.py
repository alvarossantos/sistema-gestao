from typing import cast

from django import forms

from financas import models as financas_models

from . import models


class MovimentacaoForm(forms.ModelForm):
    """Campos que não existem no model, só existem para controlar
    o parcelamento no momento da criação
    """

    class Meta:
        model = models.Movimentacao
        fields = [
            "conta",
            "categoria",
            "forma_pagamento",
            "centro_custo",
            "cartao",
            "descricao",
            "valor",
            "tipo",
            "data_movimentacao",
            "data_vencimento",
            "numero_parcela",
            "total_parcelas",
            "observacao",
        ]

        widgets = {
            "conta": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "forma_pagamento": forms.Select(attrs={"class": "form-control"}),
            "centro_custo": forms.Select(attrs={"class": "form-control"}),
            "cartao": forms.Select(attrs={"class": "form-control"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "type": "number"}
            ),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "data_movimentacao": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_vencimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "numero_parcela": forms.NumberInput(attrs={"class": "form-control"}),
            "total_parcelas": forms.NumberInput(attrs={"class": "form-control"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

        labels = {
            "conta": "Conta",
            "categoria": "Categoria",
            "forma_pagamento": "Forma de Pagamento",
            "centro_custo": "Centro de Custo",
            "cartao": "Cartão",
            "descricao": "Descrição",
            "valor": "Valor",
            "tipo": "Tipo",
            "data_movimentacao": "Data de Movimentação",
            "data_vencimento": "Data de Vencimento",
            "numero_parcela": "Número de Parcela",
            "total_parcelas": "Total de Parcelas",
            "observacao": "Observação",
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["forma_pagamento"].required = False
        self.fields["centro_custo"].required = False
        self.fields["cartao"].required = False

        if user:
            cast(
                forms.ModelChoiceField, self.fields["conta"]
            ).queryset = financas_models.Conta.objects.filter(usuario=user, ativa=True)
            cast(
                forms.ModelChoiceField, self.fields["categoria"]
            ).queryset = financas_models.Categoria.objects.filter(
                usuario=user, ativa=True
            )
            cast(
                forms.ModelChoiceField, self.fields["centro_custo"]
            ).queryset = financas_models.CentroCusto.objects.filter(
                usuario=user, ativo=True
            )
            cast(
                forms.ModelChoiceField, self.fields["cartao"]
            ).queryset = financas_models.CartaoCredito.objects.filter(usuario=user)

    def clean(self):
        cleaned_data = super().clean()
        numero_parcela = cleaned_data.get("numero_parcela")
        total_parcelas = cleaned_data.get("total_parcelas")

        if numero_parcela and not total_parcelas:
            self.add_error(
                "total_parcelas",
                "Informe em quantas parcelas deseja dividir o pagamento.",
            )

        valor = cleaned_data.get("valor")
        if valor is not None and valor <= 0:
            self.add_error("valor", "O valor deve ser maior que zero.")

        data_mov = cleaned_data.get("data_movimentacao")
        data_venc = cleaned_data.get("data_vencimento")
        if data_mov and data_venc and data_venc < data_mov:
            self.add_error(
                "data_vencimento",
                "O vencimento não pode ser antes da data da movimentação.",
            )

        return cleaned_data


class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = models.Transferencia
        fields = ["conta_origem", "conta_destino", "valor", "data", "observacao"]
        widgets = {
            "conta_origem": forms.Select(attrs={"class": "form-control"}),
            "conta_destino": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
        }
        labels = {
            "conta_origem": "Conta Origem",
            "conta_destino": "Conta Destino",
            "valor": "Valor",
            "data": "Data",
            "observacao": "Observação",
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            contas = financas_models.Conta.objects.filter(usuario=user, ativa=True)
            cast(forms.ModelChoiceField, self.fields["conta_origem"]).queryset = contas
            cast(forms.ModelChoiceField, self.fields["conta_destino"]).queryset = contas

    def clean(self):
        cleaned_data = super().clean()
        origem = cleaned_data.get("conta_origem")
        destino = cleaned_data.get("conta_destino")
        if origem and destino and origem == destino:
            self.add_error(
                "conta_destino",
                "Conta de destino não pode ser a mesma que a conta de origem.",
            )

        valor = cleaned_data.get("valor")
        if valor is not None and valor <= 0:
            self.add_error("valor", "O valor deve ser maior que zero.")

        return cleaned_data


class AnexoMovimentacaoForm(forms.ModelForm):
    class Meta:
        model = models.AnexoMovimentacao
        fields = ["movimentacao", "arquivo"]
        widgets = {
            "movimentacao": forms.Select(attrs={"class": "form-control"}),
            "arquivo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "movimentacao": "Movimentação",
            "arquivo": "Arquivo/Anexo",
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            cast(
                forms.ModelChoiceField, self.fields["movimentacao"]
            ).queryset = models.Movimentacao.objects.filter(usuario=user)
