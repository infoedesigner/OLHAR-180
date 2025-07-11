# Generated by Django 4.1.2 on 2023-02-10 13:04

from django.db import migrations


def update_clipping(apps, schema_editor):
    Clipping = apps.get_model('clients', 'Clipping')
    for clipping in Clipping.objects.all():
        clipping.publish_date = clipping.source.media.publish_date
        clipping.content = clipping.source.transcription
        clipping.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_auto_20230208_1716'),
    ]

    operations = [
        migrations.RunPython(update_clipping)
    ]
