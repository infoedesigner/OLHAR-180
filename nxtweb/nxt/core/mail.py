from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.defaultfilters import strip_tags
from django.conf import settings


def send_mail_template(subject, to, template_name, context=None, use_thread=True):
    context.update({'SITE_URL': settings.SITE_URL, 'STATIC_URL': settings.STATIC_URL})
    html = render_to_string(template_name, context)
    text = strip_tags(html)
    msg = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, to)
    msg.attach_alternative(html, "text/html")
    r = msg.send()
