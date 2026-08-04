from django.urls import path

from . import views

app_name = "financas"

urlpatterns = [
    path("listarcontas/", views.FinancasContaListView.as_view(), name="listarcontas"),
    path("listarcontas/nova/", views.FinancasContaCreateView.as_view(), name="nova"),
    path("listarcontas/<int:pk>/", views.FinancasContaDetailView.as_view(), name="detalhe"),
    path("listarcontas/<int:pk>/editar/", views.FinancasContaUpdateView.as_view(), name="editar"),

    path("listarcategorias/", views.FinancasCategoriaListView.as_view(), name="listarcategorias"),
    path("listarcategorias/nova/", views.FinancasCategoriaCreateView.as_view(), name="novacategoria"),
    path("listarcategorias/<int:pk>/", views.FinancasCategoriaDetailView.as_view(), name="detalhecategoria"),
    path("listarcategorias/<int:pk>/editar/", views.FinancasCategoriaUpdateView.as_view(), name="editarcategoria"),

    path("listarcentrocustos/", views.FinancasCentroCustoListView.as_view(), name="listarcentrocustos"),
    path("listarcentrocustos/nova/", views.FinancasCentroCustoCreateView.as_view(), name="novacentrocusto"),
    path("listarcentrocustos/<int:pk>/", views.FinancasCentroCustoDetailView.as_view(), name="detalhecentrocusto"),
    path("listarcentrocustos/<int:pk>/editar/", views.FinancasCentroCustoUpdateView.as_view(), name="editarcentrocusto"),

    path("cartao/", views.FinancasCartaoCreditoListView.as_view(), name="listarcartao"),
    path("cartao/nova/", views.FinancasCartaoCreditoCreateView.as_view(), name="novacartao"),
    path("cartao/<int:pk>/", views.FinancasCartaoCreditoDetailView.as_view(), name="detalhecartao"),
    path("cartao/<int:pk>/editar/", views.FinancasCartaoCreditoUpdateView.as_view(), name="editarcartao"),
]
