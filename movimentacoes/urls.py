from django.urls import path
from . import views

app_name = "movimentacoes"

urlpatterns = [
    # Movimentações
    path("movimentacoes/", views.MovimentacaoListView.as_view(), name="listarmovimentacao"),
    path("movimentacoes/nova/", views.MovimentacaoCreateView.as_view(), name="movimentacao-nova"),
    path("movimentacoes/<int:pk>/", views.MovimentacaoDetailView.as_view(), name="movimentacao-detalhe"),
    path("movimentacoes/<int:pk>/editar/", views.MovimentacaoUpdateView.as_view(), name="movimentacao-editar"),
    path("movimentacoes/<int:pk>/excluir/", views.MovimentacaoDeleteView.as_view(), name="movimentacao-excluir"),

    # Transferências
    path("transferencias/", views.TransferenciaListView.as_view(), name="listartransferencia"),
    path("transferencias/nova/", views.TransferenciaCreateView.as_view(), name="transferencia-nova"),
    path("transferencias/<int:pk>/", views.TransferenciaDetailView.as_view(), name="transferencia-detalhe"),
    path("transferencias/<int:pk>/editar/", views.TransferenciaUpdateView.as_view(), name="transferencia-editar"),
    path("transferencias/<int:pk>/excluir/", views.TransferenciaDeleteView.as_view(), name="transferencia-excluir"),

    # Anexos
    path("anexos/", views.AnexoMovimentacaoListView.as_view(), name="listaranexo"),
    path("anexos/nova/", views.AnexoMovimentacaoCreateView.as_view(), name="anexo-nova"),
    path("anexos/<int:pk>/", views.AnexoMovimentacaoDetailView.as_view(), name="anexo-detalhe"),
]
