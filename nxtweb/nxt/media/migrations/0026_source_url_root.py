# Generated by Django 4.1.2 on 2023-01-12 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0025_source_author_xpath_source_date_format_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='url_root',
            field=models.CharField(blank=True, max_length=255, verbose_name='Link Últimas Notícias'),
        ),
    ]
