from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class FinancasContaListView(LoginRequiredMixin, ListView):
    model = models.Conta
    template_name = "conta_list.html"
    context_object_name = "contas"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasContaCreateView(LoginRequiredMixin, CreateView):
    model = models.Conta
    template_name = "conta_create.html"
    form_class = forms.ContaForm
    success_url = reverse_lazy("financas:conta-listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasContaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Conta
    template_name = "conta_update.html"
    form_class = forms.ContaForm
    success_url = reverse_lazy("financas:conta-listar")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasContaDetailView(LoginRequiredMixin, DetailView):
    model = models.Conta
    template_name = "conta_detail.html"
    context_object_name = "conta"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasDesativarContaView(LoginRequiredMixin, View):
    template_name = "conta_desativar.html"

    def get_conta(self):
        return models.Conta.objects.filter(usuario=self.request.user).get(
            pk=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):
        conta = self.get_conta()
        return render(request, self.template_name, {"conta": conta})

    def post(self, request, *args, **kwargs):
        conta = self.get_conta()
        conta.ativa = not conta.ativa
        conta.save(update_fields=["ativa"])

        status = "ativa" if conta.ativa else "desativada"
        messages.success(request, f"Conta '{conta.nome}' {status} com sucesso.")
        return redirect(reverse_lazy("financas:conta-listar"))


class FinancasCategoriaListView(LoginRequiredMixin, ListView):
    model = models.Categoria
    template_name = "categoria_list.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCategoriaCreateView(LoginRequiredMixin, CreateView):
    model = models.Categoria
    template_name = "categoria_create.html"
    form_class = forms.CategoriaForm
    success_url = reverse_lazy("financas:categoria-listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Categoria
    template_name = "categoria_update.html"
    form_class = forms.CategoriaForm
    success_url = reverse_lazy("financas:categoria-listar")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCategoriaDetailView(LoginRequiredMixin, DetailView):
    model = models.Categoria
    template_name = "categoria_detail.html"
    context_object_name = "categoria"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasDesativarCategoriaView(LoginRequiredMixin, View):
    template_name = "categoria_desativar.html"

    def get_categoria(self):
        return models.Categoria.objects.filter(usuario=self.request.user).get(
            pk=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):
        categoria = self.get_categoria()
        return render(request, self.template_name, {"categoria": categoria})

    def post(self, request, *args, **kwargs):
        categoria = self.get_categoria()
        categoria.ativa = not categoria.ativa
        categoria.save(update_fields=["ativa"])

        status = "ativa" if categoria.ativa else "desativada"
        messages.success(request, f"Categoria '{categoria.nome}' {status} com sucesso.")
        return redirect(reverse_lazy("financas:categoria-listar"))


class FinancasCentroCustoListView(LoginRequiredMixin, ListView):
    model = models.CentroCusto
    template_name = "centrocusto_list.html"
    context_object_name = "centrocustos"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCentroCustoCreateView(LoginRequiredMixin, CreateView):
    model = models.CentroCusto
    template_name = "centrocusto_create.html"
    form_class = forms.CentroCustoForm
    success_url = reverse_lazy("financas:centrocusto-listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCentroCustoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CentroCusto
    template_name = "centrocusto_update.html"
    form_class = forms.CentroCustoForm
    success_url = reverse_lazy("financas:centrocusto-listar")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCentroCustoDetailView(LoginRequiredMixin, DetailView):
    model = models.CentroCusto
    template_name = "centrocusto_detail.html"
    context_object_name = "centrocusto"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasDesativarCentroCustoView(LoginRequiredMixin, View):
    template_name = "centrocusto_desativar.html"

    def get_centrocusto(self):
        return models.CentroCusto.objects.filter(usuario=self.request.user).get(
            pk=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):
        centrocusto = self.get_centrocusto()
        return render(request, self.template_name, {"centrocusto": centrocusto})

    def post(self, request, *args, **kwargs):
        centrocusto = self.get_centrocusto()
        centrocusto.ativo = not centrocusto.ativo
        centrocusto.save(update_fields=["ativo"])

        status = "ativa" if centrocusto.ativo else "desativada"
        messages.success(
            request, f"Centro de custo '{centrocusto.nome}' {status} com sucesso."
        )
        return redirect(reverse_lazy("financas:centrocusto-listar"))


class FinancasCartaoCreditoListView(LoginRequiredMixin, ListView):
    model = models.CartaoCredito
    template_name = "cartao_list.html"
    context_object_name = "cartao_credito"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCartaoCreditoCreateView(LoginRequiredMixin, CreateView):
    model = models.CartaoCredito
    template_name = "cartao_create.html"
    form_class = forms.CartaoCreditoForm
    success_url = reverse_lazy("financas:cartao-listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCartaoCreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CartaoCredito
    template_name = "cartao_update.html"
    form_class = forms.CartaoCreditoForm
    success_url = reverse_lazy("financas:cartao-listar")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCartaoCreditoDetailView(LoginRequiredMixin, DetailView):
    model = models.CartaoCredito
    template_name = "cartao_detail.html"
    context_object_name = "cartao_credito"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasFormaPagamentoListView(LoginRequiredMixin, ListView):
    model = models.FormaPagamento
    template_name = "forma_list.html"
    context_object_name = "forma_pagamento"


class FinancasFormaPagamentoCreateView(LoginRequiredMixin, CreateView):
    model = models.FormaPagamento
    template_name = "forma_create.html"
    form_class = forms.FormaPagamentoForm
    success_url = reverse_lazy("financas:forma-listar")


class FinancasFormaPagamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.FormaPagamento
    template_name = "forma_update.html"
    form_class = forms.FormaPagamentoForm
    success_url = reverse_lazy("financas:forma-listar")
