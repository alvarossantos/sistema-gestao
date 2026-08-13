from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name="brl")
def brl(valor):
    """Formata um valor numérico como moeda BRL: R$ 1.234,56"""
    if valor is None:
        return "R$ 0,00"
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return "R$ 0,00"
    inteiro = intcomma(int(abs(valor))).replace(",", "X").replace(".", ",").replace("X", ".")
    centavos = f"{abs(valor):.2f}".split(".")[1]
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {inteiro},{centavos}"
