from django.db import models

from ckeditor.fields import RichTextField

from nxt.core.models import BaseModel
from nxt.core.choices import STATE_CHOICES, RATING_CHOICES, MENTION_CHOICES, DATE_XPATH_CHOICES


class ClientQuerySet(models.QuerySet):

    def by_client_id(self, client_id):
        return self.filter(client__id=client_id)
    # def by_name(self, company):
    #     clients = []
    #     for client in self.filter(client__company_name=company):
    #         clients.append(client.company_name)
    #     return self.filter(company_name__in=clients)

class Client(BaseModel):

    PROFILE_CHOICES = (
        (v, v) for v in (
            'Pessoa Jurídica', 'Pessoa Física'
        )
    )
    objects = ClientQuerySet.as_manager()

    profile = models.CharField('Perfil', max_length=20, choices=PROFILE_CHOICES)
    company_name = models.CharField('Razão Social / Nome', max_length=100)
    slug = models.CharField('Link Página do Cliente', max_length=100, unique=True)
    cnpj_cpf = models.CharField('CNPJ/CPF', max_length=18, blank=True)
    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    cell = models.CharField('Celular', max_length=20, blank=True)
    brand = models.ImageField('Logo', upload_to='clients/brand', null=True, blank=True)
    postal_code = models.CharField('CEP', max_length=9, blank=True)
    address = models.CharField('Logradouro', max_length=100, blank=True)
    number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=50, blank=True)
    city = models.ForeignKey('core.City', models.SET_NULL, null=True, blank=True, verbose_name='Cidade')
    state = models.CharField('Estado', max_length=2, blank=True, choices=STATE_CHOICES)
    observations = RichTextField(
        verbose_name='Dossiê', blank=True, help_text='Outras inforamções sobre o Cliente'
    )
    company = models.ForeignKey(
        'companies.Company', models.PROTECT, verbose_name='Empresa', related_name='clients'
    )
    created_by = models.ForeignKey(
        'security.User', models.PROTECT, verbose_name='Criado por', related_name='clients'
    )
    # sources
    sources_contract = models.ManyToManyField(
        'media.Source', blank=True, verbose_name='Contrato', related_name='clients_contract'
    )
    sources_main = models.ManyToManyField(
        'media.Source', blank=True, verbose_name='Contrato', related_name='clients_main'
    )

    def __str__(self):
        return self.company_name

    def root_categories(self):
        return self.categories.filter(parent__isnull=True, is_active=True)

    def full_address(self):
        values = [self.address, self.number, self.complement, str(self.city), self.state, self.postal_code]
        values = [value.strip() for value in values if value.strip()]
        return ' - '.join(values)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['company_name']


class CategoryQuerySet(models.QuerySet):

    def by_clipping(self, company, text):
        categories = []
        for category in self.filter(client__company=company):
            for positive in PositiveWord.objects.filter(keyword__category=category):
                if positive.word.lower() in text.lower():
                    categories.append(category.pk)
                    break
        return self.filter(pk__in=categories)


class Category(BaseModel):

    name = models.CharField('Nome', max_length=50, blank=True)
    client = models.ForeignKey(Client, models.CASCADE, verbose_name='Cliente', related_name='categories')
    parent = models.ForeignKey(
        'self', models.SET_NULL, blank=True, null=True, related_name='subcategories',
        verbose_name='Categoria'
    )
    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.name

    def active_keywords(self):
        return self.keywords.filter(is_active=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']


class Keyword(BaseModel):

    SOURCE_CHOICES = (
        (v, v) for v in (
            'Todos', 'Contrato', 'Principais', 'Off'
        )
    )
    category = models.ForeignKey(
        Category, models.CASCADE, related_name='keywords', verbose_name='Categoria'
    )
    source = models.CharField('Filtro', max_length=20, default='Todos')

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name = 'Termo'
        verbose_name_plural = 'Termos'


class PositiveWord(BaseModel):

    keyword = models.ForeignKey(Keyword, models.CASCADE, verbose_name='Termo', related_name='positives')
    word = models.CharField('Palavra', max_length=100)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Termo Positivo'
        verbose_name_plural = 'Termos Positivos'
        ordering = ['word']


class NegativeWord(BaseModel):

    keyword = models.ForeignKey(Keyword, models.CASCADE, verbose_name='Termo', related_name='negatives')
    word = models.CharField('Palavra', max_length=100)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Termo Negativo'
        verbose_name_plural = 'Termos Negativos'
        ordering = ['word']


class Clipping(BaseModel):

    keyword = models.ForeignKey(Keyword, models.SET_NULL, verbose_name='Termo', null=True, blank=True)
    keyword_used = models.CharField('Termo', max_length=50)
    category = models.ForeignKey(Category, models.CASCADE, null=True, blank=True, verbose_name='Categoria')
    text = models.TextField('Texto encontrado', blank=True)
    source = models.ForeignKey(
        'media.MediaContent', models.CASCADE, verbose_name='Fonte', related_name='clippings'
    )
    negative_words_used = models.CharField('Termo', max_length=255, blank=True)
    content = models.TextField('Conteúdo', blank=True)
    publish_date = models.DateTimeField('Data publicação')
    client = models.ForeignKey(
        Client, models.CASCADE, verbose_name='Cliente', related_name='clippings',
    )
    # reports
    has_evaluation = models.BooleanField('Avaliada', default=False)
    has_strength = models.BooleanField('Força', default=False)
    has_opportunity = models.BooleanField('Oportunidade', default=False)
    has_weakness = models.BooleanField('Fraqueza', default=False)
    has_weakness = models.BooleanField('Fraqueza', default=False)
    rating = models.CharField('Classificação', choices=RATING_CHOICES, blank=True, max_length=20)
    mention = models.CharField('Menção', choices=MENTION_CHOICES, blank=True, max_length=20)
    approved = models.BooleanField('Aprovado', default=True, blank=True)
    featured = models.BooleanField('Destaque', default=False, blank=True)
    subject = models.CharField('Assunto', max_length=100, blank=True)
    marketing_value = models.DecimalField(
        'Valoração R$', decimal_places=2, max_digits=10, null=True, blank=True
    )
    newsletter_sent = models.BooleanField('Enviado na newsletter', default=False, blank=True)

    def __str__(self):
        return f'[{self.client}] {self.keyword_used}'

    class Meta:
        verbose_name = 'Recorte'
        verbose_name_plural = 'Recortes'
        ordering = ['-publish_date', '-created']
