import uuid
from typing import cast

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from core.utils import _somar_meses
from financas.models import CartaoCredito, Categoria, Conta

from . import forms
from .models import AnexoMovimentacao, Movimentacao, Transferencia


class MovimentacaoListView(LoginRequiredMixin, ListView):
    model = Movimentacao
    template_name = "movimentacao_list.html"
    context_object_name = "movimentacoes"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            super().get_queryset()
            .filter(usuario=self.request.user)
            .select_related("conta", "categoria", "forma_pagamento", "centro_custo", "cartao")
            .order_by("-data_vencimento")
        )
        params = self.request.GET
        if q := params.get("q"):
            qs = qs.filter(descricao__icontains=q)
        if tipo := params.get("tipo"):
            qs = qs.filter(tipo=tipo)
        if status := params.get("status"):
            qs = qs.filter(status=status)
        if conta_id := params.get("conta"):
            qs = qs.filter(conta_id=conta_id)
        if cat_id := params.get("categoria"):
            qs = qs.filter(categoria_id=cat_id)
        if mes := params.get("mes"):
            ano, mes_num = mes.split("-")
            qs = qs.filter(data_movimentacao__year=ano, data_movimentacao__month=mes_num)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        movs = Movimentacao.objects.filter(usuario=user)
        meses = (
            movs.dates("data_movimentacao", "month")
            .order_by("-data_movimentacao")
            .values_list("data_movimentacao", flat=True)[:12]
        )
        context["meses"] = [d.strftime("%Y-%m") for d in meses]
        context["contas_filter"] = Conta.objects.filter(usuario=user, ativa=True)
        context["categorias_filter"] = Categoria.objects.filter(usuario=user, ativa=True)
        return context


class MovimentacaoCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacao
    template_name = "movimentacao_create.html"
    form_class = forms.MovimentacaoForm
    success_url = reverse_lazy("movimentacoes:listarmovimentacao")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        total_parcelas = form.cleaned_data.get("total_parcelas")

        if total_parcelas and total_parcelas > 1:
            form.instance.grupo_parcela = uuid.uuid4()
            form.instance.numero_parcela = 1

            # salva a 1ª parcela em self.object
            response = super().form_valid(form)
            primeira = form.instance

            novas = [
                Movimentacao(
                    usuario=primeira.usuario,
                    conta=primeira.conta,
                    categoria=primeira.categoria,
                    forma_pagamento=primeira.forma_pagamento,
                    centro_custo=primeira.centro_custo,
                    cartao=primeira.cartao,
                    descricao=primeira.descricao,
                    valor=primeira.valor,
                    tipo=primeira.tipo,
                    status="PENDENTE",
                    data_movimentacao=primeira.data_movimentacao,
                    data_vencimento=_somar_meses(primeira.data_vencimento, n - 1),
                    grupo_parcela=primeira.grupo_parcela,
                    numero_parcela=n,
                    total_parcelas=total_parcelas,
                    observacao=primeira.observacao,
                )
                for n in range(2, total_parcelas + 1)
            ]
            Movimentacao.objects.bulk_create(novas)
            messages.success(
                self.request, f"Lançamento parcelado em {total_parcelas} parcelas."
            )
            return response

        response = super().form_valid(form)
        messages.success(self.request, "Movimentação criado com sucesso.")
        return response


class MovimentacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Movimentacao
    template_name = "movimentacao_update.html"
    form_class = forms.MovimentacaoForm
    success_url = reverse_lazy("movimentacoes:listarmovimentacao")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class MovimentacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Movimentacao
    template_name = "movimentacao_confirm_delete.html"
    context_object_name = "movimentacao"
    success_url = reverse_lazy("movimentacoes:listarmovimentacao")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class MovimentacaoDetailView(LoginRequiredMixin, DetailView):
    model = Movimentacao
    template_name = "movimentacao_detail.html"
    context_object_name = "movimentacao"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class MovimentacaoPagarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        movimentacao = get_object_or_404(
            Movimentacao, pk=kwargs["pk"], usuario=request.user
        )
        movimentacao.status = "PAGO"
        movimentacao.data_pagamento = timezone.localdate()
        movimentacao.save(update_fields=["status", "data_pagamento"])
        messages.success(request, f"'{movimentacao.descricao}' marcado como paga.")
        return redirect(reverse_lazy("movimentacoes:listarmovimentacao"))


class TransferenciaListView(LoginRequiredMixin, ListView):
    model = Transferencia
    template_name = "transferencia_list.html"
    context_object_name = "transferencias"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class TransferenciaCreateView(LoginRequiredMixin, CreateView):
    model = Transferencia
    template_name = "transferencia_create.html"
    form_class = forms.TransferenciaForm
    success_url = reverse_lazy("movimentacoes:listartransferencia")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class TransferenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Transferencia
    template_name = "transferencia_update.html"
    form_class = forms.TransferenciaForm
    success_url = reverse_lazy("movimentacoes:listartransferencia")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TransferenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Transferencia
    template_name = "transferencia_confirm_delete.html"
    success_url = reverse_lazy("movimentacoes:listartransferencia")

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class TransferenciaDetailView(LoginRequiredMixin, DetailView):
    model = Transferencia
    template_name = "transferencia_detail.html"
    context_object_name = "transferencia"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class AnexoMovimentacaoListView(LoginRequiredMixin, ListView):
    model = AnexoMovimentacao
    template_name = "anexo_list.html"
    context_object_name = "anexos"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(movimentacao__usuario=self.request.user)


class AnexoMovimentacaoCreateView(LoginRequiredMixin, CreateView):
    model = AnexoMovimentacao
    template_name = "anexo_create.html"
    form_class = forms.AnexoMovimentacaoForm
    success_url = reverse_lazy("movimentacoes:listaranexo")

    def get_queryset(self):
        return super().get_queryset().filter(movimentacao__usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AnexoMovimentacaoDetailView(LoginRequiredMixin, DetailView):
    model = AnexoMovimentacao
    template_name = "anexo_detail.html"
    context_object_name = "anexo"

    def get_queryset(self):
        return super().get_queryset().filter(movimentacao__usuario=self.request.user)


class AnexoMovimentacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = AnexoMovimentacao
    template_name = "anexo_update.html"
    form_class = forms.AnexoMovimentacaoForm
    success_url = reverse_lazy("movimentacoes:listaranexo")

    def get_queryset(self):
        return super().get_queryset().filter(movimentacao__usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AnexoMovimentacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = AnexoMovimentacao
    template_name = "anexo_confirm_delete.html"
    context_object_name = "anexo"
    success_url = reverse_lazy("movimentacoes:listaranexo")

    def get_queryset(self):
        return super().get_queryset().filter(movimentacao__usuario=self.request.user)

    def form_valid(self, form):
        self.object = cast(AnexoMovimentacao, self.get_object())
        self.object.arquivo.delete(save=False)
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
