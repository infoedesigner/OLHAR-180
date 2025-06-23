import random

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager as BaseUserManager, PermissionsMixin
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from localflavor.br.models import BRCPFField

from nxt.core.models import BaseModel
from nxt.core.choices import (
    MARITAL_STATUS_CHOICES, PIX_KEY_TYPE_CHOICES, STATE_CHOICES, DEGREE_CHOICES
)

from nxt.mailer.models import Message


class NXTPermission(BaseModel):

    name = models.CharField('Nome', max_length=50)
    code = models.SlugField('Código', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Permissão NXT'
        verbose_name_plural = 'Permissões NXT'
        ordering = ['id']

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given cpf and password.
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    PROFILE_CHOICES = (
        ('administrador', 'Administrador'),
        ('funcionario', 'Funcionário'),
        ('cliente', 'Cliente'),
    )

    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=50)
    expiration = models.DateField('Data de Expiração', null=True, blank=True)
    client = models.ForeignKey(
        'clients.Client', models.CASCADE, null=True, blank=True, related_name='users',
        verbose_name='Cliente'
    )
    profile = models.CharField(
        'Perfil', choices=PROFILE_CHOICES, max_length=20, default='cliente'
    )
    company = models.ForeignKey(
        'companies.Company', models.SET_NULL, null=True, blank=True, related_name='users'
    )
    companies = models.ManyToManyField(
        'companies.Company', blank=True, related_name='total_users', verbose_name='Todas as Empresas'
    )
    created_by = models.ForeignKey(
        'self', models.SET_NULL, null=True, blank=True, verbose_name='Criado por',
    )
    # address
    postal_code = models.CharField('CEP', max_length=9, blank=True)
    address = models.CharField('Logradouro', max_length=100, blank=True)
    number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=50, blank=True)
    neighborhood = models.CharField('Bairro', max_length=50, blank=True)
    city = models.ForeignKey(
        'core.City', models.SET_NULL, null=True, blank=True, verbose_name='Cidade', related_name='users'
    )
    state = models.CharField('Estado', max_length=2, choices=STATE_CHOICES, blank=True)
    # bank
    bank = models.ForeignKey(
        'core.Bank', models.SET_NULL, null=True, blank=True, verbose_name='Banco',
        related_name='users_bank'
    )
    bank_agency = models.CharField('Agência', max_length=10, blank=True)
    bank_number = models.CharField('Conta', max_length=10, blank=True)
    bank_operation = models.CharField('Operação', max_length=50, blank=True)
    bank_pix1 = models.ForeignKey(
        'core.Bank', models.SET_NULL, null=True, blank=True, verbose_name='Banco',
        related_name='users_bank_pix1'
    )
    bank_pix1_key_type = models.CharField(
        'Tipo da Chave', max_length=20, choices=PIX_KEY_TYPE_CHOICES, blank=True
    )
    bank_pix1_value = models.CharField('Valor', max_length=50, blank=True)
    bank_pix2 = models.ForeignKey(
        'core.Bank', models.SET_NULL, null=True, blank=True, verbose_name='Banco',
        related_name='users_bank_pix2'
    )
    bank_pix2_key_type = models.CharField(
        'Tipo da Chave', max_length=20, choices=PIX_KEY_TYPE_CHOICES, blank=True,
    )
    bank_pix2_value = models.CharField('Valor', max_length=50, blank=True)
    # others
    birth_date = models.DateField('Data de Nascimento', null=True, blank=True)
    mothers_name = models.CharField('Nome da Mãe', max_length=50, blank=True)
    fathers_name = models.CharField('Nome do Pai', max_length=50, blank=True)
    naturalness = models.ForeignKey(
        'core.City', models.SET_NULL, null=True, blank=False, related_name='naturalness_users'
    )
    naturalness_uf = models.CharField('UF Naturalidade', max_length=2, blank=True, choices=STATE_CHOICES)
    degree = models.CharField('Escolaridade', max_length=30, blank=True, choices=DEGREE_CHOICES)
    marital_status = models.CharField(
        'Estado Civil', max_length=30, blank=True, choices=MARITAL_STATUS_CHOICES
    )
    # children
    number_of_children = models.PositiveSmallIntegerField('Números de filhos', default=0)
    childrens_names = models.CharField('Nome dos Filhos', max_length=255, blank=True)
    childrens_cpfs = models.CharField('CPF filho(s)', max_length=100, blank=True)
    # documents
    cpf = BRCPFField(verbose_name='CPF', blank=True)
    rg = models.CharField('RG', max_length=10, blank=True)
    rg_entity_uf = models.CharField('Órgão Expedidor/UF', max_length=50, blank=True)
    rg_expedition = models.DateField('Data de emissão', null=True, blank=True)
    work_card = models.CharField('Carteira de Trabalho', max_length=20, blank=True)
    pis_pasep = models.CharField('Pis/Pasep', max_length=20, blank=True)
    voter_registration = models.CharField('Título de Eleitor', blank=True, max_length=20)
    driver_card = models.CharField('Número da Carteira de Motorista', max_length=20, blank=True)
    driver_card_entity_uf = models.CharField('Órgão Expedidor/UF', max_length=50, blank=True)
    driver_card_expedition = models.DateField('Data da emissão', null=True, blank=True)
    # contact
    phone = models.CharField('Telefone Celular', max_length=15, blank=True)
    home_phone = models.CharField('Telefone Residencial', max_length=15, blank=True)
    whatsapp = models.CharField('Whatsapp', max_length=15, blank=True)
    phone_message = models.CharField('Telefone Recardo', max_length=15, blank=True)
    phone_contact = models.TextField(
        'Informe telefone de parentes ou outros meios que possam ser utilizados para contato '
        'com o (a) colaborador (a), colocar telefone, nome e grau de parentesco:',
        blank=True
    )
    photo = models.ImageField('Foto', upload_to='users/photos', null=True, blank=True)
    # internet
    internet_type = models.CharField(
        'Tipo de Internet', help_text='Banda Larga/fibra', blank=True, max_length=30
    )
    internet_provider = models.CharField('Provedor', max_length=50, blank=True)
    internet_contracted_speed = models.CharField('Velocidade Contratada', max_length=50, blank=True)
    internet_download_speed = models.CharField('Velocidade Download', max_length=50, blank=True)
    internet_upload_speed = models.CharField('Velocidade Upload', max_length=50, blank=True)
    internet_others_providers = models.CharField('Outra opções de provedor', max_length=100, blank=True)
    internet_cost = models.CharField('Valor de ajuda de custo', max_length=50, blank=True)
    # equipament
    has_equipament = models.BooleanField('Possui Equipamento', default=False)
    equipament_type = models.CharField('Tipo', help_text='PC/Notebook', blank=True, max_length=50)
    equipament_brand = models.CharField('Marca', max_length=50, blank=True)
    equipament_model = models.CharField('Modelo', max_length=50, blank=True)
    equipament_processor = models.CharField('Processador', max_length=50, blank=True)
    equipament_memory = models.CharField('Memória', max_length=50, blank=True)
    equipament_hd = models.CharField('HD', max_length=50, blank=True)
    equipament_brand = models.CharField('Marca', max_length=50, blank=True)
    equipament_hd_used = models.CharField('Espaço em Uso', max_length=50, blank=True)
    equipament_has_dvr = models.BooleanField('Possui DVR', default=False)
    equipament_dvr_number = models.CharField('Número de DVRs', max_length=50, blank=True)
    equipament_dvr_description = models.CharField('Marca/modelo/descrição', max_length=100, blank=True)
    equipament_dvr_status = models.CharField(
        'Situação', max_length=50, blank=True, help_text='em uso/parado/queimado/estragado'
    )
    equipament_dvr_local = models.CharField('Local', max_length=50, blank=True)
    equipament_dvr_local_recorded = models.TextField('Canais gravados', blank=True)
    equipament_dvr_total_channels = models.CharField('Número total de canais', max_length=50, blank=True)
    # admin
    nxt_permissions = models.ManyToManyField(NXTPermission, blank=True)
    is_staff = models.BooleanField('Equipe', default=False)
    last_access = models.DateTimeField('Último acesso', null=True, blank=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return self.name.split()[0]

    def uidb64(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['name']


class ResetPassword(BaseModel):

    user = models.ForeignKey(User, models.CASCADE, verbose_name='Usuário', related_name='resets')
    code = models.CharField('Código', max_length=10)
    used = models.BooleanField('Usado', default=False)

    def __str__(self):
        return f'{self.user}: {self.code}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(1000, 9999))
        return super().save(*args, **kwargs)

    def send_mail(self):
        Message.objects.create_message(
            'Seu código de Recuperação de Senha', self.user.email, 'security/emails/reset_password.html',
            {'reset_password': self}
        )

    class Meta:
        verbose_name = 'Recuperação de Senha'
        verbose_name_plural = 'Recuperações de Senha'
        ordering = ['-created']


def pre_save_user(instance, **kwargs):
    if instance.is_staff:
        instance.profile = 'administrador'


def post_save_reset_password(instance, created, **kwargs):
    if created:
        instance.send_mail()


models.signals.pre_save.connect(pre_save_user, sender=User, dispatch_uid='pre_save_user')
models.signals.post_save.connect(
    post_save_reset_password, sender=ResetPassword, dispatch_uid='post_save_reset_password'
)
