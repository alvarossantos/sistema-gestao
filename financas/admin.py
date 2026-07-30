from django.contrib import admin
from . import models


admin.site.register(models.Conta)
admin.site.register(models.CartaoCredito)
admin.site.register(models.Categoria)
admin.site.register(models.CentroCusto)
admin.site.register(models.FormaPagamento)
