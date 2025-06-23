from django.db import models

from nxt.core.choices import STATE_CHOICES, DOCUMENT_TYPE_CHOICES
from nxt.core.models import BaseModel

from nxt.media.gazette import load_gazette


class Company(BaseModel):

    company_name = models.CharField('Razão Social', max_length=100)
    brand_name = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    state_registration = models.CharField('Inscrição Estadual', max_length=20, blank=True)
    county_registration = models.CharField('Inscrição Municipal', max_length=20, blank=True)
    postal_code = models.CharField('CEP', max_length=9, blank=True)
    address = models.CharField('Logradouro', max_length=100, blank=True)
    number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=50, blank=True)
    city = models.CharField('Cidade', max_length=50, blank=True)
    state = models.CharField('Estado', max_length=2, blank=True, choices=STATE_CHOICES)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Document(BaseModel):

    company = models.ForeignKey(Company, models.CASCADE, verbose_name='Empresa', related_name='documents')
    document_type = models.CharField('Tipo do Documento', max_length=100, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField('Título', max_length=100)
    reference_date = models.DateField('Data de Referência')
    start_date = models.DateField('Válido de')
    end_date = models.DateField('Até a data', null=True, blank=True)
    document_file = models.FileField('Arquivo', upload_to='companies/documents')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-created']


def post_save_company(instance, created, **kwargs):
    if created:
        load_gazette(instance)


models.signals.post_save.connect(post_save_company, sender=Company, dispatch_uid='post_save_company')
