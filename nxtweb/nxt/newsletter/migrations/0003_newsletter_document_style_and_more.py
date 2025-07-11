# Generated by Django 4.1.2 on 2023-03-22 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0022_alter_clipping_source'),
        ('newsletter', '0002_newsletter_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='document_style',
            field=models.TextField(blank=True, verbose_name='Estilo Documento'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='document_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Documento'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='footer_style',
            field=models.TextField(blank=True, verbose_name='Estilo Rodapé'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='footer_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Rodapé'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='general_style',
            field=models.TextField(blank=True, verbose_name='Estilo Geral'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='general_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Geral'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='header_style',
            field=models.TextField(blank=True, verbose_name='Estilo Cabeçalho'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='header_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Cabeçalho'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='link_style',
            field=models.TextField(blank=True, verbose_name='Estilo Link da Notícia'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='link_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Link da Notícia'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='media_style',
            field=models.TextField(blank=True, verbose_name='Estilo Mídia'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='media_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Mídia'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='news_layout',
            field=models.CharField(choices=[('Categoria', 'Categoria'), ('Data da notícia', 'Data da notícia'), ('Data da notícia - Decrescente', 'Data da notícia - Decrescente'), ('Data de cadastro', 'Data de cadastro'), ('Data de cadastro - Decrescente', 'Data de cadastro - Decrescente'), ('Mídia » Veículo » Página » Data de cadastro', 'Mídia » Veículo » Página » Data de cadastro')], default='Mídia » Veículo » Página » Data de cadastro', max_length=100, verbose_name='Disposição das Notícias'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='resume_style',
            field=models.TextField(blank=True, verbose_name='Estilo Resumo'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='resume_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Resumo'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='segmentation',
            field=models.CharField(choices=[('Sem segmentação', 'Sem segmentação'), ('Segmentado por veículo', 'Segmentado por veículo'), ('Segmentado por categoria', 'Segmentado por categoria'), ('Segmentado por mídia', 'Segmentado por mídia'), ('Segmentado por categoria/veículo', 'Segmentado por categoria/veículo'), ('Segmentado por categoria/mídia/veículo', 'Segmentado por categoria/mídia/veículo'), ('Segmentado por veículo/categoria', 'Segmentado por veículo/categoria'), ('Segmentado por mídia/veículo', 'Segmentado por mídia/veículo'), ('Segmentado por mídia/veículo/categoria', 'Segmentado por mídia/veículo/categoria'), ('Segmentado por mídia/categoria/veículo', 'Segmentado por mídia/categoria/veículo')], default='Sem segmentação', max_length=50, verbose_name='Forma de Visualização'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='title_style',
            field=models.TextField(blank=True, verbose_name='Estilo Título'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='title_style_active',
            field=models.BooleanField(default=False, verbose_name='Estilo Título'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newsletters', to='clients.category', verbose_name='Categoria'),
        ),
    ]
