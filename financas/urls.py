from django.urls import path

from . import views

app_name = "financas"

urlpatterns = [
    path("listarcontas/", views.FinancasContaListView.as_view(), name="listarcontas"),
    path("listarcontas/nova/", views.FinancasContaCreateView.as_view(), name="nova"),
    path("listarcontas/<int:pk>/", views.FinancasContaDetailView.as_view(), name="detalhe"),
    path("listarcontas/<int:pk>/editar/", views.FinancasContaUpdateView.as_view(), name="editar"),
    
]
