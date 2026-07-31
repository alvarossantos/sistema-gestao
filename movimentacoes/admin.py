from django.contrib import admin

from .models import Movimentacao, Transferencia, AnexoMovimentacao


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'status', 'data_movimentacao', 'data_vencimento', 'conta', 'categoria')
    list_filter = ('tipo', 'status', 'data_movimentacao', 'conta', 'categoria')
    search_fields = ('descricao', 'observacao')
    list_editable = ('status',)
    readonly_fields = ('criado_em',)
    ordering = ('-data_movimentacao',)
    date_hierarchy = 'data_movimentacao'


@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('conta_origem', 'conta_destino', 'valor', 'data')
    list_filter = ('data',)
    search_fields = ('observacao',)
    readonly_fields = ('criado_em',)
    ordering = ('-data',)


@admin.register(AnexoMovimentacao)
class AnexoMovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'movimentacao', 'enviado_em')
    list_filter = ('enviado_em',)
    search_fields = ('arquivo',)
    readonly_fields = ('enviado_em',)
