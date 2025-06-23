from celery import shared_task


@shared_task
def send_message(message_id):
    from nxt.mailer.models import Message
    message = Message.objects.get(pk=message_id)
    message.send_mail()
