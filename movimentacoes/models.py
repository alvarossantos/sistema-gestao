from typing import ClassVar

from django.db import models


class Movimentacao(models.Model):
    TIPO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    conta = models.ForeignKey('financas.Conta', on_delete=models.PROTECT)
    categoria = models.ForeignKey('financas.Categoria', on_delete=models.PROTECT)
    forma_pagamento = models.ForeignKey('financas.FormaPagamento', on_delete=models.SET_NULL, blank=True, null=True, db_column='formas_pagamento_id')
    centro_custo = models.ForeignKey('financas.CentroCusto', on_delete=models.SET_NULL, blank=True, null=True, db_column='centros_custo_id')
    cartao = models.ForeignKey('financas.CartaoCredito', on_delete=models.SET_NULL, blank=True, null=True)

    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')

    data_movimentacao = models.DateField()
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)

    grupo_parcela = models.UUIDField(blank=True, null=True)
    numero_parcela = models.IntegerField(blank=True, null=True)
    total_parcelas = models.IntegerField(blank=True, null=True)

    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'movimentacao'

    def __str__(self):
        return str(self.descricao)


class Transferencia(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    conta_origem = models.ForeignKey('financas.Conta', on_delete=models.PROTECT, related_name='transferencias_origem')
    conta_destino = models.ForeignKey('financas.Conta', on_delete=models.PROTECT, related_name='transferencias_destino')

    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'transferencia'

    def __str__(self):
        return f"Transferência {self.valor}"


class AnexoMovimentacao(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to="anexos/")
    enviado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'anexo_movimentacao'

    def __str__(self):
        return str(self.arquivo)
