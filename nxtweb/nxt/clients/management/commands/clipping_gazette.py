import re
import datetime as dt

from django.core.management.base import BaseCommand

from nxt.media.models import Source, Media, MediaContent

from nxt.clients.models import Keyword, Clipping


class Command(BaseCommand):

    def handle(self, *args, **options):
        for keyword in Keyword.objects.exclude(source='Off'):
            if keyword.source == 'Todos':
                sources = Source.objects.filter(company=keyword.category.client.company)
            elif keyword.source == 'Contrato':
                sources = keyword.category.client.sources_contract.all()
            elif keyword.source == 'Principais':
                sources = keyword.category.client.sources_main.all()
            else:
                sources = Source.objects.none()
            today = dt.datetime.now()
            start = dt.datetime(today.year, today.month, today.day)
            end = start + dt.timedelta(days=1)
            medias = Media.objects.filter(source__in=sources)
            medias = medias.filter(publish_date__gte=start, publish_date__lt=end)
            media_contents = MediaContent.objects.filter(
                transcription__icontains=keyword.word
            )
            for media_content in media_contents:
                occurrences = re.finditer(keyword.word, media_content.transcription)
                for occurrence in occurrences:
                    start = max(0, occurrence.start() - 50)
                    end = min(len(media_content.transcription), occurrence.start() + 50)
                    Clipping.objects.create(
                        keyword_used=keyword.word, text=media_content.transcription[start:end],
                        negative_words_used='', source=media_content, client=keyword.category.client,
                        category=keyword.category
                    )
