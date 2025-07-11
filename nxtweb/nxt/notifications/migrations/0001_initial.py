# Generated by Django 4.1.2 on 2023-02-08 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0005_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('title', models.CharField(max_length=100, verbose_name='Título do Modelo')),
                ('notification_type', models.CharField(choices=[('Newsletter', 'Newsletter'), ('Recuperação de Senha', 'Recuperação de Senha'), ('Validação de Senha', 'Validação de Senha')], max_length=40, verbose_name='Tipo da Modelo')),
                ('content', models.TextField(verbose_name='Conteúdo')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='Empresa')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('notification_type', models.CharField(choices=[], max_length=40, verbose_name='Tipo da Notificação')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('read', models.BooleanField(default=False, verbose_name='Lida')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='Empresa')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
                'ordering': ['-created'],
            },
        ),
    ]
