# Generated by Django 4.1.2 on 2022-12-17 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0019_alter_editorial_date_format'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editorial',
            options={'ordering': ['name'], 'verbose_name': 'Editoria', 'verbose_name_plural': 'Editoria'},
        ),
        migrations.AddField(
            model_name='editorial',
            name='frequency',
            field=models.CharField(blank=True, choices=[], max_length=20, verbose_name='Periodicidade'),
        ),
        migrations.AddField(
            model_name='editorial',
            name='marketing_value',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Vl publicit. padrão'),
        ),
        migrations.AlterField(
            model_name='editorial',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome da Editoria'),
        ),
        migrations.AlterField(
            model_name='editorial',
            name='url',
            field=models.CharField(default='', max_length=255, verbose_name='Link da Editoria'),
        ),
    ]
