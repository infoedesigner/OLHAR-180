# Generated by Django 4.1.2 on 2023-03-16 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0035_newspaper_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediacontent',
            name='newspaper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.newspaper', verbose_name='Selecione o Impresso'),
        ),
        migrations.AddField(
            model_name='mediacontent',
            name='newspaper_crop',
            field=models.TextField(blank=True, verbose_name='Capa'),
        ),
        migrations.AddField(
            model_name='mediacontent',
            name='newspaper_page',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Número da Página'),
        ),
    ]
