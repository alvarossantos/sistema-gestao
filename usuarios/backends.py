from django.contrib.auth.hashers import check_password

from .models import Usuario


class UsuarioBackend:
    """
    Backend de autenticação customizado que usa a tabela 'usuario'
    em vez da tabela padrão 'auth_user' do Django.
    """

    # Autentica o usuário com base no nome de usuário e senha, retornando o usuário se a senha estiver correta
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

        if check_password(password, usuario.password_hash):
            return usuario
        return None

    # Obtém o usuário com base no ID, retornando o usuário se existir
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
