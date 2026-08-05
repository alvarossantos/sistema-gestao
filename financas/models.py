from decimal import Decimal
from typing import ClassVar

from django.db import models
from django.db.models import Sum

from core.utils import _somar_meses, _dia_no_mes

from django.utils import timezone
from datetime import timedelta


class Conta(models.Model):
    # ClassVar: indica que é uma constante de classe, evitando warning do type checker
    TIPO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("CAIXA", "Caixa"),
        ("CORRENTE", "Corrente"),
        ("POUPANCA", "Poupanca"),
        ("CARTEIRA", "Carteira"),
        ("INVESTIMENTO", "Investimento"),
    ]
    usuario = models.ForeignKey("usuarios.Usuario", models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "conta"

    def __str__(self):
        return str(self.nome)

    def get_saldo_atual(self):
        from movimentacoes.models import Movimentacao, Transferencia

        movimentacoes = Movimentacao.objects.filter(
            conta=self, status="PAGO", cartao__isnull=True
        )
        receitas = movimentacoes.filter(tipo="RECEITA").aggregate(total=Sum("valor"))[
            "total"
        ] or Decimal("0")
        despesas = movimentacoes.filter(tipo="DESPESA").aggregate(total=Sum("valor"))[
            "total"
        ] or Decimal("0")

        recebidas = Transferencia.objects.filter(conta_destino=self).aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0")
        enviadas = Transferencia.objects.filter(conta_origem=self).aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0")

        return self.saldo_inicial + receitas - despesas + recebidas - enviadas


class CartaoCredito(models.Model):
    usuario = models.ForeignKey("usuarios.Usuario", models.CASCADE)
    nome = models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=12, decimal_places=2)
    dia_fechamento = models.IntegerField()
    dia_vencimento = models.IntegerField()
    conta_pagamento = models.ForeignKey("Conta", models.CASCADE)

    class Meta:
        managed = False
        db_table = "cartao_credito"

    def __str__(self):
        return str(self.nome)

    def get_periodo_fatura_atual(self, referencia=None):
        referencia = referencia or timezone.localdate()
        fechamento = _dia_no_mes(referencia.year, referencia.month, self.dia_fechamento)

        if referencia > fechamento:
            fechamento = _somar_meses(fechamento, 1)

        inicio = _somar_meses(fechamento, -1) + timedelta(days=1)

        if self.dia_vencimento < self.dia_fechamento:
            vencimento = _somar_meses(_dia_no_mes(fechamento.year, fechamento.month, self.dia_vencimento), 1)
        else:
            vencimento = _dia_no_mes(fechamento.year, fechamento.month, self.dia_vencimento)

        return inicio, fechamento, vencimento

    def get_valor_fatura_digital(self):
        from movimentacoes.models import Movimentacao

        inicio, fechamento, _ = self.get_periodo_fatura_atual()
        total = (
            Movimentacao.objects.filter(
                cartao=self, tipo="DESPESA",
                data_movimentacao__gte=inicio, data_movimentacao__lte=fechamento,
            )
            .exclude(tipo="CANCELADO")
            .aggregate(total=Sum("valor"))["total"]
        )
        return total or Decimal("0")


class Categoria(models.Model):
    # ClassVar: indica que é uma constante de classe, evitando warning do type checker
    TIPO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("RECEITA", "Receita"),
        ("DESPESA", "Despesa"),
    ]
    usuario = models.ForeignKey("usuarios.Usuario", models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria_pai = models.ForeignKey("self", models.SET_NULL, blank=True, null=True)
    cor = models.CharField(max_length=7)
    ativa = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "categoria"

    def __str__(self):
        return str(self.nome)


class CentroCusto(models.Model):
    usuario = models.ForeignKey("usuarios.Usuario", models.CASCADE)
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "centro_custo"

    def __str__(self):
        return str(self.nome)


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "forma_pagamento"

    def __str__(self):
        return str(self.nome)
