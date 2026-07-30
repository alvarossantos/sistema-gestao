from enum import unique
from pickletools import unicodestring1
from tokenize import blank_re

from django.db import models
from django.forms.formsets import ORDERING_FIELD_NAME
from typing_extensions import OrderedDict

import manage

class Usuario(models.Model):
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=128)
    primeiro_nome = models.CharField(max_length=150)
    ultimo_nome = models.CharField(max_length=150)
    foto = models.TextField(blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    ultimo_login = models.DateField(blank=True, null=True)
    ativo = models.BooleanField()
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
        ordering = ['username']
