import calendar
from datetime import date


def _somar_meses(data, meses):
    """
    dia 31/jan + 1 mês -> 28/29 de fev, sem estourar erro de data inválida
    """
    mes_index = data.month - 1 + meses
    ano = data.year + mes_index // 12
    mes = mes_index % 12 + 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return data.replace(year=ano, month=mes, day=dia)


def _dia_no_mes(ano, mes, dia):
    dia_valido = min(dia, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia_valido)
