from typing import ClassVar

from django.db import models


class Conta(models.Model):
    # ClassVar: indica que é uma constante de classe, evitando warning do type checker
    TIPO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('CAIXA', 'Caixa'),
        ('CORRENTE', 'Corrente'),
        ('POUPANCA', 'Poupanca'),
        ('CARTEIRA', 'Carteira'),
        ('INVESTIMENTO', 'Investimento'),
    ]
    usuario = models.ForeignKey('usuarios.Usuario', models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conta'

    def __str__(self):
        return str(self.nome)

class CartaoCredito(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', models.CASCADE)
    nome = models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=12, decimal_places=2)
    dia_fechamento = models.IntegerField()
    dia_vencimento = models.IntegerField()
    conta_pagamento = models.ForeignKey('Conta', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cartao_credito'

    def __str__(self):
        return str(self.nome)

class Categoria(models.Model):
    # ClassVar: indica que é uma constante de classe, evitando warning do type checker
    TIPO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    usuario = models.ForeignKey('usuarios.Usuario', models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria_pai = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)
    cor = models.CharField(max_length=7)
    ativa = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
        return str(self.nome)

class CentroCusto(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', models.CASCADE)
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'centro_custo'

    def __str__(self):
        return str(self.nome)

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'forma_pagamento'

    def __str__(self):
        return str(self.nome)
