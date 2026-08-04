from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import forms, models


class FinancasContaListView(LoginRequiredMixin, ListView):
    model = models.Conta
    template_name = "contas_list.html"
    context_object_name = "contas"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasContaCreateView(LoginRequiredMixin, CreateView):
    model = models.Conta
    template_name = "contas_create.html"
    form_class = forms.ContaForm
    success_url = reverse_lazy("financas:listarcontas")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasContaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Conta
    template_name = "contas_update.html"
    form_class = forms.ContaForm
    success_url = reverse_lazy("financas:listarcontas")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasContaDetailView(LoginRequiredMixin, DetailView):
    model = models.Conta
    template_name = "contas_detail.html"
    context_object_name = "conta"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)
