import json
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
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

        # ── Saldo total das contas (1 query, sem N+1) ──────────────────
        contas = Conta.objects.filter(usuario=usuario, ativa=True)

        # Busca totais de movimentações pagas (sem cartão) por conta em batch
        mov_por_conta = (
            Movimentacao.objects.filter(
                usuario=usuario,
                status="PAGO",
                cartao__isnull=True,
            )
            .values("conta_id")
            .annotate(
                receitas=Sum("valor", filter=Q(tipo="RECEITA")),
                despesas=Sum("valor", filter=Q(tipo="DESPESA")),
            )
        )
        # Indexa por conta_id para lookup O(1)
        agg_por_conta = {
            row["conta_id"]: row
            for row in mov_por_conta
        }

        # Busca transferências por conta em batch
        from movimentacoes.models import Transferencia

        transf_destino = (
            Transferencia.objects.filter(usuario=usuario)
            .values("conta_destino_id")
            .annotate(total=Sum("valor"))
        )
        transf_origem = (
            Transferencia.objects.filter(usuario=usuario)
            .values("conta_origem_id")
            .annotate(total=Sum("valor"))
        )
        agg_transf_dest = {r["conta_destino_id"]: r["total"] or Decimal("0") for r in transf_destino}
        agg_transf_orig = {r["conta_origem_id"]: r["total"] or Decimal("0") for r in transf_origem}

        saldo_total = Decimal("0")
        for conta in contas:
            movs = agg_por_conta.get(conta.pk, {})
            receitas = movs.get("receitas") or Decimal("0")
            despesas = movs.get("despesas") or Decimal("0")
            recebidas = agg_transf_dest.get(conta.pk, Decimal("0"))
            enviadas = agg_transf_orig.get(conta.pk, Decimal("0"))
            saldo_total += conta.saldo_inicial + receitas - despesas + recebidas - enviadas

        # ── Resumo do mês ─────────────────────────────────────────────
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

        # ── Próximos vencimentos ──────────────────────────────────────
        proximos_vencimentos = (
            Movimentacao.objects.filter(
                usuario=usuario,
                status="PENDENTE",
                data_vencimento__gte=hoje,
            )
            .select_related("conta", "categoria", "forma_pagamento", "cartao")
            .order_by("data_vencimento")[:5]
        )

        # ── Faturas dos cartões ───────────────────────────────────────
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

        # ── Dados para gráficos Chart.js ──────────────────────────────
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
                receitas=Sum("valor", filter=Q(tipo="RECEITA")),
                despesas=Sum("valor", filter=Q(tipo="DESPESA")),
            )
            meses_receitas.append(float(stats["receitas"] or 0))
            meses_despesas.append(float(stats["despesas"] or 0))

        # ── Top categorias por despesa no mês ─────────────────────────
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
