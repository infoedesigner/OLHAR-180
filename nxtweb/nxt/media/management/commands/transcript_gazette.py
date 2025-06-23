import pdfplumber
import traceback

from django.core.management.base import BaseCommand

from nxt.media.models import MediaContent


class Command(BaseCommand):

    def handle(self, *args, **options):
        media_contents = MediaContent.objects.filter(
            processed=False, document__isnull=False,
        )
        for media_content in media_contents:
            print(f'Media: {media_content}')
            media_content.processed = True
            try:
                with pdfplumber.open(media_content.document.path) as pdf_file:
                    contents = []
                    for page in pdf_file.pages:
                        content = page.extract_text()
                        contents.append(content)
                    contents = '\n'.join([c for c in contents])
                    media_content.transcription = contents
            except Exception as ex:
                media_content.errors = traceback.format_exc()
            try:
                media_content.save()
            except Exception as ex:
                pass
