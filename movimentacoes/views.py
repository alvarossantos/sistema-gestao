from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms
from .models import AnexoMovimentacao, Movimentacao, Transferencia


class MovimentacaoListView(LoginRequiredMixin, ListView):
    model = Movimentacao
    template_name = "movimentacao_list.html"
    context_object_name = "movimentacoes"

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


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
        return super().form_valid(form)


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


class TransferenciaListView(LoginRequiredMixin, ListView):
    model = Transferencia
    template_name = "transferencia_list.html"
    context_object_name = "transferencias"

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
