# Generated by Django 4.1.2 on 2022-11-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0013_alter_media_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Título'),
        ),
    ]
