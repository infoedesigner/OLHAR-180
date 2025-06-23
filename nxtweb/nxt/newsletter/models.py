import datetime as dt

from django.db import models
from django.utils import timezone
from django.utils.formats import date_format

from nxt.core.choices import (
    DAY_CHOICES, SEGMENTATION_CHOICES, NEWS_LAYOUT_CHOICES, NEWSLETTER_LAYOUT_CHOICES
)

from nxt.core.models import BaseModel
from nxt.mailer.models import Message
from nxt.clients.models import Clipping, Category


class Contact(BaseModel):
    """
    Model representing a contact that can receive a newsletter.
    """

    # A foreign key to the `Client` model from the `clients` app
    client = models.ForeignKey(
        'clients.Client', models.CASCADE, verbose_name='Cliente', related_name='contacts'
    )

    # An email field for the contact's email address
    email = models.EmailField('E-mail')

    # A name field for the contact's name
    name = models.CharField('Nome', max_length=100, blank=True)

    def __str__(self):
        """
        Returns the email address of the contact.
        """
        return self.email

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['email']

class Newsletter(BaseModel):
    """
    Model representing a newsletter that can be sent to one or more contacts.
    """

#FIELDS###

    # A foreign key to the `Client` model from the `clients` app
    client = models.ForeignKey(
        'clients.Client', models.CASCADE, verbose_name='Cliente', related_name='newsletters'
    )

    # A title field for the newsletter
    title = models.CharField('Título', max_length=100)

    # A foreign key to the `Category` model from the `clients` app
    categories = models.ManyToManyField(
    'clients.Category', blank=True, verbose_name='Categorias', related_name='newsletters',  )

    # A field for defining the segmentation of the newsletter
    segmentation = models.CharField(
        'Forma de Visualização', choices=SEGMENTATION_CHOICES, default='Sem segmentação',
        max_length=50
    )

    # A field for defining the layout of news in the newsletter
    news_layout = models.CharField(
        'Disposição das Notícias', choices=NEWS_LAYOUT_CHOICES, max_length=100,
        default='Mídia » Veículo » Página » Data de cadastro'
    )

    # A field for defining the layout of the newsletter itself
    newsletter_layout = models.CharField(
        'Layout', choices=NEWSLETTER_LAYOUT_CHOICES, max_length=100,
        default='CATEGORIA COM CORES PERSONALIZADAS'
    )

#STYLES###
    document_style = models.TextField('Estilo Documento', blank=True)
    document_style_active = models.BooleanField('Estilo Documento', default=False)
    general_style = models.TextField('Estilo Geral', blank=True)
    general_style_active = models.BooleanField('Estilo Geral', default=False)
    header_style = models.TextField('Estilo Cabeçalho', blank=True)
    header_style_active = models.BooleanField('Estilo Cabeçalho', default=False)
    footer_style = models.TextField('Estilo Rodapé', blank=True)
    footer_style_active = models.BooleanField('Estilo Rodapé', default=False)
    title_style = models.TextField('Estilo Título', blank=True)
    title_style_active = models.BooleanField('Estilo Título', default=False)
    media_style = models.TextField('Estilo Mídia', blank=True)
    media_style_active = models.BooleanField('Estilo Mídia', default=False)
    link_style = models.TextField('Estilo Link da Notícia', blank=True)
    link_style_active = models.BooleanField('Estilo Link da Notícia', default=False)
    resume_style = models.TextField('Estilo Resumo', blank=True)
    resume_style_active = models.BooleanField('Estilo Resumo', default=False)
##STYLES END####

    contacts = models.ManyToManyField(
        Contact, blank=True, related_name='newsletters', verbose_name='Contatos'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

class Schedule(BaseModel):
    newsletter = models.ForeignKey(
        Newsletter, models.CASCADE, verbose_name='Agenda', related_name='schedules'
    )
    day = models.PositiveSmallIntegerField('Dia', choices=DAY_CHOICES)
    time = models.TimeField('Horário')

    def __str__(self):
        return f'{self.newsletter} {self.day} [{self.time}]'

    def send_newsletter(self):
        """
        Send the newsletter to all contacts associated with the newsletter, 
        and update the Clipping objects.
        """

        # Creates a ScheduleHistory object to keep track of when the newsletter was sent
        history = ScheduleHistory.objects.create(schedule=self)
        now = timezone.now()
        # Limit the Clipping objects to those created within the last 3 days
        limit_date = now - dt.timedelta(days=3)
        clippings = Clipping.objects.filter(newsletter_sent=False, created__gte=limit_date)
        categories = Category.objects.all()
        # Format the date and time for the newsletter title
        date = dt.datetime(now.date(), self.time.hour, self.time.minute)
        date = date_format(date, 'd/m/Y H:i')
        title = f'{self.newsletter.title} {date}'
        # Create a dictionary with the necessary context for the newsletter email
        context = {
            'categories': categories,
            'clippings': clippings,
            'title': title,
            'client': self.newsletter.client,
        }
        # Loop through each contact associated with the newsletter and send the email
        for contact in self.newsletter.contacts.all():
            context_contact = context.copy()
            context_contact['contact'] = contact
            Message.objects.create_message(
                subject=title, recipient=contact.email, template_name='newsletter/emails/newsletter.html',
                context=context_contact
            )
        # Update the Clipping objects to mark them as sent and update the history object
        history.finished = timezone.now()
        history.save()
        clippings.update(newsletter_sent=True)

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        ordering = ['day', 'time']

class ScheduleHistory(BaseModel):
    schedule = models.ForeignKey(Schedule, models.CASCADE, verbose_name='Agenda')
    finished = models.DateTimeField('Finalizada', null=True, blank=True)

    def __str__(self):
        return f'{self.schedule}'

    class Meta:
        verbose_name = 'Histórico de Agenda Newsletter'
        verbose_name_plural = 'Históricos de Agenda Newsletter'
        ordering = ['-created']
