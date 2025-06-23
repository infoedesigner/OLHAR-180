import os
import re
import threading
import pdf2image
import datetime as dt

from django.db import models
from django.conf import settings
from django.utils import timezone

from nxt.core.models import BaseModel
from nxt.core.choices import STATE_CHOICES, FREQUENCY_CHOICES, DATE_XPATH_CHOICES

from nxt.clients.models import Keyword, Clipping, PositiveWord

from nxt.media.clipping import clipping_paragraph

class Source(BaseModel):

    SOURCE_TYPE_CHOICES = [
        ('diariooficial', 'Diário Oficial'),
        ('tv', 'TV'),
        ('radio', 'Rádio'),
        ('site', 'Site'),
        ('blog', 'Blog'),
        ('impresso', 'Impresso'),
        ('revista', 'Revista'),
    ]

    name = models.CharField('Nome do Veículo', max_length=50)
    source_type = models.CharField('Tipo do Veículo', choices=SOURCE_TYPE_CHOICES, max_length=30)
    territory_id = models.CharField('Id do Território', max_length=10)
    priority = models.BooleanField('Prioritário', default=False)
    marketing_value = models.DecimalField(
        'Vl publicit. padrão', null=True, blank=True, decimal_places=2, max_digits=8
    )
    company = models.ForeignKey(
        'companies.Company', models.CASCADE, verbose_name='Empresa', related_name='sources'
    )
    city = models.ForeignKey('core.City', models.SET_NULL, null=True, verbose_name='Cidade')
    state = models.CharField('Estado', max_length=2, choices=STATE_CHOICES)
    website = models.CharField('Endereço do Site', max_length=255, blank=True)
    frequency = models.CharField('Periodicidade', max_length=20, blank=True, choices=FREQUENCY_CHOICES)
    publish_days = models.JSONField(verbose_name='Dias de Publicação', null=True, blank=True)
    audience = models.PositiveIntegerField('Quantiade de público', null=True, blank=True)
    # sites
    url_root = models.CharField('Link Últimas Notícias', max_length=255, blank=True)
    url_xpath = models.CharField('Caminho para o Link', max_length=100, blank=True)
    date_xpath = models.CharField('Caminho para a Data', max_length=100, blank=True)
    date_format = models.CharField('Formato da data', max_length=50, choices=DATE_XPATH_CHOICES, blank=True)
    title_xpath = models.CharField('Caminho para o Título', max_length=100, blank=True)
    headline_xpath = models.CharField('Caminho para o Resumo/Subtítulo', max_length=100, blank=True)
    author_xpath = models.CharField('Caminho para o Autor', max_length=100, blank=True)
    text_xpath = models.CharField('Caminho para o Texto', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Veículo de Informação'
        verbose_name_plural = 'Veículos de Informações'
        ordering = ['name']


class Editorial(BaseModel):

    source = models.ForeignKey(Source, models.CASCADE, verbose_name='Veículo', related_name='editorials')
    name = models.CharField('Nome da Editoria', max_length=100)
    marketing_value = models.PositiveIntegerField('Vl publicit. padrão', null=True, blank=True)
    frequency = models.CharField('Periodicidade', max_length=20, blank=True, choices=FREQUENCY_CHOICES)
    use_configuration_source = models.BooleanField('Usar Configuração do Veículo', default=True)
    url = models.CharField('Link da Editoria', max_length=255, blank=True)
    url_xpath = models.CharField('Caminho para o Link', max_length=100, blank=True)
    date_xpath = models.CharField('Caminho para a Data', max_length=100, blank=True)
    date_format = models.CharField('Formato da data', max_length=50, choices=DATE_XPATH_CHOICES, blank=True)
    title_xpath = models.CharField('Caminho para o Título', max_length=100, blank=True)
    headline_xpath = models.CharField('Caminho para o Resumo/Subtítulo', max_length=100, blank=True)
    author_xpath = models.CharField('Caminho para o Autor', max_length=100, blank=True)
    text_xpath = models.CharField('Caminho para o Texto', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Editoria'
        verbose_name_plural = 'Editoria'
        ordering = ['name']


class Newspaper(BaseModel):

    company = models.ForeignKey(
        'companies.Company', models.CASCADE, verbose_name='Empresa', related_name='newspapers'
    )
    source = models.ForeignKey(Source, models.CASCADE, verbose_name='Veículo', related_name='newspapers')
    pdf_file = models.FileField('Arquivo PDF', upload_to='media/newspaper')
    publish_date = models.DateField('Data Publicação')

    def __str__(self):
        return f'{self.source}: {self.publish_date}'

    class Meta:
        verbose_name = 'Impresso'
        verbose_name_plural = 'Impressos'
        ordering = ['-publish_date']


class Media(BaseModel):

    MEDIA_TYPE_CHOICES = [
        (v, v) for v in (
            'ANÚNCIO/PUBLICIDADE',
            'AO VIVO E CHAMADA',
            'ARTIGO',
            'CARTA/EMAIL',
            'CHAMADA DE CAPA',
            'CHARGE',
            'CINEMA',
            'COLUNA',
            'CRÔNICA',
            'CURTAS',
            'DEBATE',
            'EDITAL',
            'EDITORIAL',
            'ENTREVISTA',
            'ESCALADA',
            'FEED',
            'IGTV',
            'INSERÇÃO ELEITORAL',
            'MATÉRIA',
            'MATÉRIA COM CHAMADA',
            'NOTA',
            'PROGRAMA ELEITORAL',
            'REPORTAGEM',
            'STORIES',
        )
    ]

    title = models.CharField('Título', max_length=255)
    media_content_type = models.CharField(
        'Tipo da Notícia', max_length=50, choices=MEDIA_TYPE_CHOICES, blank=True
    )
    url = models.CharField('Link do Conteúdo', blank=True, max_length=255)
    source = models.ForeignKey(Source, models.CASCADE, verbose_name='Veículo', related_name='medias')
    editorial = models.ForeignKey(Editorial, models.SET_NULL, null=True, blank=True, verbose_name='editorial')
    publish_date = models.DateTimeField('Data Publicação')
    publish_date_raw = models.CharField('Data Publicação (texto)', max_length=255, blank=True)
    resume = models.CharField('Resumo', max_length=255, blank=True)
    authors = models.CharField(
        'Autores', max_length=255, blank=True, help_text='Use vírgula para separar os autores'
    )
    image = models.CharField('Imagem', blank=True, max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        now = dt.datetime.now()
        if not self.publish_date:
            try:
                self.publish_date = dt.datetime.strptime(
                    self.publish_date_raw, self.editorial.date_xpath
                )
            except:
                dates = re.findall('([0-2][0-9]\/[0-1][0-9]\/\d{4})', self.publish_date_raw)
                for date in dates:
                    try:
                        date = dt.datetime.strptime(date, 'd/m/Y')
                    except:
                        continue
                    if date < now:
                        self.publish_date = date
                        break
                if not self.publish_date:
                    self.publish_date = timezone.now()
        return super().save(*args, **kwargs)

    def clippings(self):
        return Clipping.objects.filter(source__in=self.contents.values('pk'))

    class Meta:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'
        ordering = ['-publish_date']


class MediaContent(BaseModel):

    media = models.ForeignKey(
        Media, models.CASCADE, verbose_name='Conteúdo da Mídia', related_name='contents'
    )
    order = models.PositiveSmallIntegerField('Ordem', default=1)
    document = models.FileField('Documento', upload_to='media/document', blank=True, null=True)
    transcription = models.TextField('Transcrição', blank=True)
    processed = models.BooleanField('Processado', default=False, blank=True)
    errors = models.TextField('Erros de Processamento', blank=True)
    processed_clipping = models.BooleanField('Processado Recorte', default=False)
    # newspaper
    newspaper_crop = models.TextField('Capa', blank=True)
    newspaper = models.ForeignKey(
        Newspaper, models.SET_NULL, blank=True, null=True, verbose_name='Selecione o Impresso'
    )
    newspaper_page = models.PositiveSmallIntegerField('Número da Página', null=True, blank=True)

    def __str__(self):
        return f'{self.media}: {self.order}'

    def process_clipping(self):
        self.processed_clipping = True
        keywords = Keyword.objects.filter(
            is_active=True, category__client__company=self.media.source.company
        )
        keywords = keywords.exclude(source='Off')
        for keyword in keywords:
            sources = None
            if keyword.source == 'Contrato':
                sources = keyword.category.client.sources_contract.all()
            elif keyword.source == 'Principais':
                sources = keyword.category.client.sources_main.all()
            if sources and self.media.source not in sources:
                continue
            save = False
            for positive in keyword.positives.all():
                clipping = clipping_paragraph(self.transcription, positive.word)
                if clipping:
                    save = True
                    break
            if not save:
                continue
            for negative in keyword.negatives.all():
                negative_word = negative.word.strip().lower()
                if negative_word and negative_word in clipping.lower():
                    save = False
                    break
            clipping_exists = Clipping.objects.filter(
                client=keyword.category.client, source=self
            )
            if save and not clipping_exists.exists():
                Clipping.objects.create(
                    keyword_used=positive.word, text=clipping, client=keyword.category.client,
                    negative_words_used=', '.join(negative.word for negative in keyword.negatives.all()),
                    source=self, category=keyword.category, keyword=keyword,
                    publish_date=self.media.publish_date, content=self.transcription
                )
        self.save()

    class Meta:
        verbose_name = 'Conteúdo da Mídia'
        verbose_name_plural = 'Conteúdos das Mídia'
        ordering = ['order']


def post_save_source(instance, created, **kwargs):
    if created and instance.url_root:
        command = f'venv/bin/scrapy crawl nxt_news -a source_id={instance.pk}'
        def run_crawler():
            os.system(
                f'cd {settings.NXT_CRAWLER_PATH} && {settings.NXT_CRAWLER_PATH}{command}'
            )
        # threading.Thread(target=run_crawler).start()


def post_save_editorial(instance, created, **kwargs):
    start = (
        not instance.use_configuration_source and created and instance.source.source_type == 'site'
        and instance.source.website
    )
    if start:
        command = f'venv/bin/scrapy crawl nxt_news -a source_id={instance.source.pk}'
        def run_crawler():
            os.system(
                f'cd {settings.NXT_CRAWLER_PATH} && {settings.NXT_CRAWLER_PATH}{command}'
            )
        # threading.Thread(target=run_crawler).start()


def post_save_media_content(instance, **kwargs):
    if not instance.processed_clipping and instance.processed:
        instance.process_clipping()


def post_save_newspaper(instance, **kwargs):
    def _proccess():
        media_dir = settings.MEDIA_ROOT
        newspaper_dir = os.path.join(media_dir, 'media', 'newspaper', str(instance.pk))
        if not os.path.exists(newspaper_dir):
            os.makedirs(newspaper_dir)
        images = pdf2image.convert_from_path(instance.pdf_file.path)
        for i, image in enumerate(images):
            page = i + 1
            image.save(f'{newspaper_dir}/{page}.png')
    threading.Thread(target=_proccess).start()


models.signals.post_save.connect(post_save_editorial, sender=Editorial, dispatch_uid='post_save_editorial')
models.signals.post_save.connect(
    post_save_media_content, sender=MediaContent, dispatch_uid='post_save_media_content'
)
models.signals.post_save.connect(
    post_save_newspaper, sender=Newspaper, dispatch_uid='post_save_newspaper'
)
