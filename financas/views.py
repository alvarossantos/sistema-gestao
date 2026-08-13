from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
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
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        contas_ativas = models.Conta.objects.filter(usuario=user, ativa=True)
        context["contas_ativas"] = contas_ativas.count()
        context["saldo_geral"] = sum(c.get_saldo_atual() for c in contas_ativas)
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saldo_atual"] = self.object.get_saldo_atual()
        return context


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
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).order_by("tipo", "nome")


class FinancasCategoriaCreateView(LoginRequiredMixin, CreateView):
    model = models.Categoria
    template_name = "categoria_create.html"
    form_class = forms.CategoriaForm
    success_url = reverse_lazy("financas:categoria-listar")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    


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
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).order_by("nome")


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
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user).select_related("conta_pagamento").order_by("nome")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartao = self.object
        inicio, fechamento, vencimento = cartao.get_periodo_fatura_atual()
        valor_fatura = cartao.get_valor_fatura_digital()
        limite_usado = cartao.limite - valor_fatura if valor_fatura else cartao.limite
        percentual_uso = (valor_fatura / cartao.limite * 100) if cartao.limite and valor_fatura else 0

        from movimentacoes.models import Movimentacao
        movimentacoes_fatura = Movimentacao.objects.filter(
            cartao=cartao,
            tipo="DESPESA",
            data_movimentacao__gte=inicio,
            data_movimentacao__lte=fechamento,
        ).exclude(status="CANCELADO").select_related("categoria").order_by("-data_movimentacao")

        context["valor_fatura"] = valor_fatura
        context["periodo_inicio"] = inicio
        context["periodo_fechamento"] = fechamento
        context["periodo_vencimento"] = vencimento
        context["limite_disponivel"] = limite_usado
        context["percentual_uso"] = percentual_uso
        context["movimentacoes_fatura"] = movimentacoes_fatura
        context["alerta_limite"] = percentual_uso >= 80
        return context


class PagarFaturaView(LoginRequiredMixin, View):
    """Paga a fatura do cartão criando uma movimentação de despesa na conta de pagamento."""

    def post(self, request, *args, **kwargs):
        cartao = get_object_or_404(
            models.CartaoCredito, pk=kwargs["pk"], usuario=request.user
        )

        valor_fatura = cartao.get_valor_fatura_digital()
        if valor_fatura <= 0:
            messages.warning(request, "Não há fatura a pagar para este cartão.")
            return redirect("financas:cartao-detalhe", pk=cartao.pk)

        from movimentacoes.models import Movimentacao

        with transaction.atomic():
            # Cria a movimentação de pagamento da fatura
            Movimentacao.objects.create(
                usuario=request.user,
                conta=cartao.conta_pagamento,
                categoria=models.Categoria.objects.filter(
                    usuario=request.user, tipo="DESPESA"
                ).first(),  # Usa a primeira categoria de despesa disponível
                descricao=f"Pagamento fatura {cartao.nome}",
                valor=valor_fatura,
                tipo="DESPESA",
                status="PAGO",
                data_movimentacao=timezone.localdate(),
                data_vencimento=timezone.localdate(),
                cartao=cartao,
                observacao=f"Pagamento automático da fatura do cartão {cartao.nome}",
            )

        messages.success(
            request,
            f"Fatura de R$ {valor_fatura:,.2f} paga com sucesso! "
            f"Valor debitado de '{cartao.conta_pagamento}'.",
        )
        return redirect("financas:cartao-detalhe", pk=cartao.pk)


class FinancasFormaPagamentoListView(LoginRequiredMixin, ListView):
    model = models.FormaPagamento
    template_name = "forma_list.html"
    context_object_name = "forma_pagamento"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().order_by("nome")


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
