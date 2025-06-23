from django.db import models

from ckeditor.fields import RichTextField

from nxt.core.models import BaseModel
from nxt.core.choices import NOTIFICATION_TYPE_CHOICES


class NotificationModel(BaseModel):

    title = models.CharField('Título do Modelo', max_length=100)
    notification_type = models.CharField(
        'Tipo da Modelo', max_length=40, choices=NOTIFICATION_TYPE_CHOICES
    )
    content = RichTextField(verbose_name='Conteúdo', blank=True)
    company = models.ForeignKey('companies.Company', models.CASCADE, verbose_name='Empresa')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Modelo de Notificação'
        verbose_name_plural = 'Modelo de Notificações'
        ordering = ['-modified']


class Notification(BaseModel):

    title = models.CharField('Título', max_length=100)
    notification_type = models.CharField(
        'Tipo da Notificação', max_length=40, choices=NOTIFICATION_TYPE_CHOICES
    )
    user = models.ForeignKey(
        'security.User', models.SET_NULL, verbose_name='Usuário', related_name='notifications',
        null=True, blank=True
    )
    email = models.EmailField('E-mail')
    read = models.BooleanField('Lida', default=False)
    company = models.ForeignKey('companies.Company', models.CASCADE, verbose_name='Empresa')

    def __str__(self):
        return f'[{self.email}] {self.title}'

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created']
