from django.urls import path

from . import views

app_name = "financas"

urlpatterns = [
    # Contas
    path("listarcontas/", views.FinancasContaListView.as_view(), name="conta-listar"),
    path("listarcontas/nova/", views.FinancasContaCreateView.as_view(), name="conta-nova"),
    path("listarcontas/<int:pk>/", views.FinancasContaDetailView.as_view(), name="conta-detalhe"),
    path("listarcontas/<int:pk>/editar/", views.FinancasContaUpdateView.as_view(), name="conta-editar"),
    path("listarcontas/<int:pk>/desativar/", views.FinancasDesativarContaView.as_view(), name="conta-desativar"),

    # Categorias
    path("listarcategorias/", views.FinancasCategoriaListView.as_view(), name="categoria-listar"),
    path("listarcategorias/nova/", views.FinancasCategoriaCreateView.as_view(), name="categoria-nova"),
    path("listarcategorias/<int:pk>/", views.FinancasCategoriaDetailView.as_view(), name="categoria-detalhe"),
    path("listarcategorias/<int:pk>/editar/", views.FinancasCategoriaUpdateView.as_view(), name="categoria-editar"),
    path("listarcategorias/<int:pk>/desativar/", views.FinancasDesativarCategoriaView.as_view(), name="categoria-desativar"),

    # Centros de Custo
    path("listarcentrocustos/", views.FinancasCentroCustoListView.as_view(), name="centrocusto-listar"),
    path("listarcentrocustos/nova/", views.FinancasCentroCustoCreateView.as_view(), name="centrocusto-nova"),
    path("listarcentrocustos/<int:pk>/", views.FinancasCentroCustoDetailView.as_view(), name="centrocusto-detalhe"),
    path("listarcentrocustos/<int:pk>/editar/", views.FinancasCentroCustoUpdateView.as_view(), name="centrocusto-editar"),
    path("listarcentrocustos/<int:pk>/desativar/", views.FinancasDesativarCentroCustoView.as_view(), name="centrocusto-desativar"),

    # Cartões de Crédito
    path("cartao/", views.FinancasCartaoCreditoListView.as_view(), name="cartao-listar"),
    path("cartao/nova/", views.FinancasCartaoCreditoCreateView.as_view(), name="cartao-nova"),
    path("cartao/<int:pk>/", views.FinancasCartaoCreditoDetailView.as_view(), name="cartao-detalhe"),
    path("cartao/<int:pk>/editar/", views.FinancasCartaoCreditoUpdateView.as_view(), name="cartao-editar"),

    # Formas de Pagamento
    path("forma/", views.FinancasFormaPagamentoListView.as_view(), name="forma-listar"),
    path("forma/nova/", views.FinancasFormaPagamentoCreateView.as_view(), name="forma-nova"),
    path("forma/<int:pk>/editar/", views.FinancasFormaPagamentoUpdateView.as_view(), name="forma-editar"),
]
