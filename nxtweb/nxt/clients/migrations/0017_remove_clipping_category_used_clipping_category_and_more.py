# Generated by Django 4.1.2 on 2023-01-20 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_city'),
        ('clients', '0016_client_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clipping',
            name='category_used',
        ),
        migrations.AddField(
            model_name='clipping',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.city', verbose_name='Cidade'),
        ),
    ]
