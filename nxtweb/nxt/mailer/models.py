from django.db import models

from nxt.core.models import BaseModel
from nxt.core.choices import EMAIL_STATUS_CHOICES
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.defaultfilters import strip_tags
from django.conf import settings

from nxt.mailer.converter import email_to_db, db_to_email
from nxt.mailer.tasks import send_message


class MessageQuerySet(models.QuerySet):

    def create_message(self, subject, recipient, template_name, context=None, sender=settings.DEFAULT_FROM_EMAIL):
        if context is None:
            context = {}
        context.update({'SITE_URL': settings.SITE_URL, 'STATIC_URL': settings.STATIC_URL})
        html = render_to_string(template_name, context)
        text = strip_tags(html)
        email = EmailMultiAlternatives(subject, text, sender, [recipient])
        email.attach_alternative(html, "text/html")
        message = Message(subject=subject, recipient=recipient, sender=sender)
        message.body = email_to_db(email)
        message.save()
        send_message.delay(message.pk)


class Message(BaseModel):

    sender = models.EmailField('Remetente')
    recipient = models.EmailField('Destinatário')
    subject = models.CharField('Assunto', max_length=100)
    body = models.TextField('Conteúdo', blank=True)
    status = models.CharField('Situação', choices=EMAIL_STATUS_CHOICES, max_length=20, default='pending')

    objects = MessageQuerySet.as_manager()

    def __str__(self):
        return f'[{self.recipient}] {self.subject}'

    def send_mail(self):
        email = db_to_email(self.body)
        email.send()

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-created']
