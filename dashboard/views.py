from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from financas.models import CartaoCredito, Conta
from movimentacoes.models import Movimentacao


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        hoje = timezone.localdate

        contas = Conta.objects.filter(usuario=usuario, ativa=True)
        saldo_total = sum(conta.get_saldo_atual() for conta in contas)

        movimentacoes_mes = Movimentacao.objects.filter(
            usuario=usuario,
            status="PAGO",
            data_movimentacao__year=hoje.year,
            data_movimentacao__month=hoje.month,
        )
        receitas_mes = movimentacoes_mes.filter(tipo="RECEITA").aggregate(total=Sum('valor'))['total'] or 0
        despesas_mes = movimentacoes_mes.filter(tipo="DESPESA").aggregate(total=Sum('valor'))['total'] or 0

        proximos_vencimentos = Movimentacao.objects.filter(
            usuario=usuario,
            status="PENDENTE",
            data_movimentacao__gte=hoje,
        ).order_by('data_vencimento')[:5]

        cartoes = CartaoCredito.objects.filter(usuario=usuario)
        faturas = [
            {
                "cartao": cartao,
                "valor": cartao.get_saldo_atual(),
                "vencimento": cartao.get_periodo_vencimento(),
            }
        ]
        
        return context
