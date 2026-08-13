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
        hoje = timezone.localdate()

        # Otimização: evita N+1 ao usar select_related no get_saldo_atual
        contas = Conta.objects.filter(usuario=usuario, ativa=True)
        saldo_total = sum(
            conta.get_saldo_atual() for conta in contas
        )

        movimentacoes_mes = Movimentacao.objects.filter(
            usuario=usuario,
            status="PAGO",
            data_movimentacao__year=hoje.year,
            data_movimentacao__month=hoje.month,
        )
        receitas_mes = (
            movimentacoes_mes.filter(tipo="RECEITA").aggregate(total=Sum("valor"))[
                "total"
            ]
            or 0
        )
        despesas_mes = (
            movimentacoes_mes.filter(tipo="DESPESA").aggregate(total=Sum("valor"))[
                "total"
            ]
            or 0
        )

        proximos_vencimentos = (
            Movimentacao.objects.filter(
                usuario=usuario,
                status="PENDENTE",
                data_vencimento__gte=hoje,
            )
            .select_related("conta", "categoria", "forma_pagamento", "cartao")
            .order_by("data_vencimento")[:5]
        )

        # Otimização: busca cartões e faturas em batch
        cartoes = CartaoCredito.objects.filter(usuario=usuario).select_related(
            "conta_pagamento"
        )
        faturas = []
        for cartao in cartoes:
            valor = cartao.get_valor_fatura_digital()
            periodo = cartao.get_periodo_fatura_atual()
            faturas.append(
                {
                    "cartao": cartao,
                    "valor": valor,
                    "vencimento": periodo,
                }
            )

        # Dados para gráficos Chart.js
        meses_labels = []
        meses_receitas = []
        meses_despesas = []
        for i in range(5, -1, -1):
            mes_ref = hoje.month - i
            ano_ref = hoje.year
            while mes_ref <= 0:
                mes_ref += 12
                ano_ref -= 1
            meses_labels.append(f"{ano_ref}-{mes_ref:02d}")
            stats = Movimentacao.objects.filter(
                usuario=usuario,
                status="PAGO",
                data_movimentacao__year=ano_ref,
                data_movimentacao__month=mes_ref,
            ).aggregate(
                receitas=Sum("valor", filter__tipo="RECEITA"),
                despesas=Sum("valor", filter__tipo="DESPESA"),
            )
            meses_receitas.append(float(stats["receitas"] or 0))
            meses_despesas.append(float(stats["despesas"] or 0))

        # Top categorias por despesa no mês
        from django.db.models import Q
        top_categorias = (
            Movimentacao.objects.filter(
                usuario=usuario,
                tipo="DESPESA",
                status="PAGO",
                data_movimentacao__year=hoje.year,
                data_movimentacao__month=hoje.month,
            )
            .values("categoria__nome", "categoria__cor")
            .annotate(total=Sum("valor"))
            .order_by("-total")[:5]
        )

        context["saldo_total"] = saldo_total
        context["receitas_mes"] = receitas_mes
        context["despesas_mes"] = despesas_mes
        context["proximos_vencimentos"] = proximos_vencimentos
        context["faturas"] = faturas
        # Dados JSON para Chart.js
        import json
        context["chart_labels"] = json.dumps(meses_labels)
        context["chart_receitas"] = json.dumps(meses_receitas)
        context["chart_despesas"] = json.dumps(meses_despesas)
        context["chart_categorias_labels"] = json.dumps(
            [c["categoria__nome"] or "Sem categoria" for c in top_categorias]
        )
        context["chart_categorias_valores"] = json.dumps(
            [float(c["total"]) for c in top_categorias]
        )
        context["chart_categorias_cores"] = json.dumps(
            [c["categoria__cor"] or "#6c757d" for c in top_categorias]
        )
        return context
