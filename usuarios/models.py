from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=128)
    primeiro_nome = models.CharField(max_length=150)
    ultimo_nome = models.CharField(max_length=150)
    foto = models.ImageField(upload_to="fotos/", blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    last_login = models.DateTimeField(blank=True, null=True, db_column='ultimo_login')
    ativo = models.BooleanField()
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
        ordering = ['username']

    def __str__(self):
        return f"{str(self.primeiro_nome)} {str(self.ultimo_nome)}"

    @property
    def is_authenticated(self):
        """Necessário para o Django reconhecer como usuário autenticado."""
        return True

    @property
    def is_active(self):
        """Mapeia o campo 'ativo' para o padrão do Django."""
        return self.ativo
