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


class FinancasCategoriaListView(LoginRequiredMixin, ListView):
    model = models.Categoria
    template_name = "categorias_list.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCategoriaCreateView(LoginRequiredMixin, CreateView):
    model = models.Categoria
    template_name = "categorias_create.html"
    form_class = forms.CategoriaForm
    success_url = reverse_lazy("financas:listarcategorias")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Categoria
    template_name = "categorias_update.html"
    form_class = forms.CategoriaForm
    success_url = reverse_lazy("financas:listarcategorias")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCategoriaDetailView(LoginRequiredMixin, DetailView):
    model = models.Categoria
    template_name = "categorias_detail.html"
    context_object_name = "categoria"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCentroCustoListView(LoginRequiredMixin, ListView):
    model = models.CentroCusto
    template_name = "centrocustos_list.html"
    context_object_name = "centrocustos"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCentroCustoCreateView(LoginRequiredMixin, CreateView):
    model = models.CentroCusto
    template_name = "centrocustos_create.html"
    form_class = forms.CentroCustoForm
    success_url = reverse_lazy("financas:listarcentrocustos")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCentroCustoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CentroCusto
    template_name = "centrocustos_update.html"
    form_class = forms.CentroCustoForm
    success_url = reverse_lazy("financas:listarcentrocustos")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCentroCustoDetailView(LoginRequiredMixin, DetailView):
    model = models.CentroCusto
    template_name = "centrocustos_detail.html"
    context_object_name = "centrocusto"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCartaoCreditoListView(LoginRequiredMixin, ListView):
    model = models.CartaoCredito
    template_name = "cartao_credito_list.html"
    context_object_name = "cartao_credito"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FinancasCartaoCreditoCreateView(LoginRequiredMixin, CreateView):
    model = models.CartaoCredito
    template_name = "cartao_credito_create.html"
    form_class = forms.CartaoCreditoForm
    success_url = reverse_lazy("financas:listarcartao")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCartaoCreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CartaoCredito
    template_name = "cartao_credito_update.html"
    form_class = forms.CartaoCreditoForm
    success_url = reverse_lazy("financas:listarcartao")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class FinancasCartaoCreditoDetailView(LoginRequiredMixin, DetailView):
    model = models.CartaoCredito
    template_name = "cartao_credito_detail.html"
    context_object_name = "cartao_credito"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)
