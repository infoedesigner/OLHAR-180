import io
import pandas as pd

from django.utils.formats import date_format
from django.conf import settings
from django.urls import reverse


def export_clippings(client, queryset):
    data = []
    for clipping in queryset:
        clipping_url = reverse('clients:clipping_detail', kwargs={'pk': clipping.pk, 'slug': client.slug})
        data.append({
            'Título': clipping.source.media.title,
            'Veículo': clipping.source.media.source,
            'Data Publicação': date_format(clipping.source.media.publish_date, 'd/m/Y H:i'),
            'Data do Clipping': date_format(clipping.created, 'd/m/Y H:i'),
            'Categoria': clipping.category.name,
            'Link': f'{settings.SITE_URL}{clipping_url}'
        })
    df = pd.DataFrame(data)
    with io.BytesIO() as output:
        excel = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(excel, index=False)
        excel.save()
        content = output.getvalue()
    return content