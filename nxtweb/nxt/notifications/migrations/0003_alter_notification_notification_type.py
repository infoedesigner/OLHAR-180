# Generated by Django 4.1.2 on 2023-02-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notificationmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Newsletter', 'Newsletter'), ('Recuperação de Senha', 'Recuperação de Senha'), ('Validação de Senha', 'Validação de Senha')], max_length=40, verbose_name='Tipo da Notificação'),
        ),
    ]
