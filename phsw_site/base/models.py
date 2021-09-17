from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CPFField, CNPJField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from phsw_site import settings


class UserManager(BaseUserManager):
    use_in_migrations = True  # essa variavel de classe serve para que possamos utilizar esse manager na migraçao.

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:  # se email nao estiver definido lança um erro
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)  # normalizamos o e-mail
        user = self.model(email=email, **extra_fields)  # cria o modelo 'user'
        user.password = make_password(password)  # seta o password pra o modelo 'user'   -----------------?
        user.save(using=self._db)  # salva o modelo no banco de dados.
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):  # ------------------?
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base User Class

    Email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)  # seta o email para indentificar o usuario
    cpf = CPFField(masked=True, blank=True, verbose_name="CPF")
    fk_empresa = models.ForeignKey('Empresa', blank=True, on_delete=models.PROTECT, null=True, verbose_name="Empresa")
    is_agente_admin = models.BooleanField(default=False)
    all_api_permissions = models.BooleanField(default=False)

    is_staff = models.BooleanField(  # essa propriedade define os usuarios que podem acessar o admin do django
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(  # essa propriedade define o usuario que pode se logar dentro do sistema
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)  # define quando o usuario entrou

    objects = UserManager()  # conectar o manager com o modelo user

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or
    # password as these fields will always be prompted for.

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Empresa(models.Model):
    tipo_choices = (
        ("D", "Distribuidora"),
        ("L", "Lojista"),
        ("O", "Outros")
    )
    status_choices = (
        ("A", "Ativado"),
        ("D", "Desativado"),
        ("B", "Bloqueado"),
    )
    fk_tabelaPreco = models.ForeignKey('pedidos.TabelaPreco', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="Tabela preço")
    nome_empresa = models.CharField(max_length=60, verbose_name="Empresa")
    cnpj = CNPJField(masked=True, blank=True, verbose_name="CNPJ")
    codigo_cliente = models.CharField(blank=True, max_length=9, verbose_name="Código do cliente")
    codigo_vendedor = models.CharField(blank=True, max_length=9, verbose_name="Código do vendedor")
    # fk_statusEmpresa = models.ForeignKey('StatusEmpresa', on_delete=models.DO_NOTHING, verbose_name="Status")
    # fk_tipoEmpresa = models.ForeignKey('TipoEmpresa', on_delete=models.DO_NOTHING, verbose_name="Tipo de empresa")
    statusEmpresa = models.CharField(max_length=1, choices=status_choices)
    tipoEmpresa = models.CharField(max_length=1, choices=tipo_choices)

    def __str__(self):
        return f'Empresa: {self.nome_empresa}'

#
# class StatusEmpresa(models.Model):
#     descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
#     verbose_name = models.CharField(max_length=15, verbose_name="Nome")
#
#     def __str__(self):
#         return f'Status: {self.verbose_name}'


# class TipoEmpresa(models.Model):
#     descricao = models.CharField(max_length=100, verbose_name="Descrição")
#     verbose_name = models.CharField(max_length=15, verbose_name="Nome")
#
#     def __str__(self):
#         return f'Tipo de empresa: {self.verbose_name}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # every time a user was created, a token will be generated fo that user.

