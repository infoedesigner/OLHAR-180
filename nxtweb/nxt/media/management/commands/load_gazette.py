import datetime as dt

from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files.base import File

from nxt.media.models import Media, MediaContent, Source


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str)
        parser.add_argument('--date', type=str)

    def handle(self, *args, **options):
        sources = Source.objects.filter(source_type='diariooficial')
        data_dir = options['data_dir']
        date_desc = options.get('date')
        if date_desc:
            date = dt.datetime.strptime(date_desc, '%Y-%m-%d')
        else:
            date = dt.datetime.now()
            date_desc = date.strftime('%Y-%m-%d')
        for source in sources:
            print(f'Source: {source}')
            path = Path(data_dir) / source.territory_id / date_desc
            media = Media.objects.filter(
                source=source, publish_date__year=date.year, publish_date__month=date.month,
                publish_date__day=date.day
            ).first()
            if media:
                continue
            media, created = Media.objects.get_or_create(
                title=f'{source.name} - {date_desc}', source=source,
                publish_date=dt.datetime(date.year, date.month, date.day)
            )
            if not created:
                continue
            try:
                exists_pdf = False
                for i, pdf_path in enumerate(path.iterdir()):
                    print(f'Path: {pdf_path}')
                    media_content = MediaContent(media=media, order=i)
                    with pdf_path.open('rb') as pdf_file:
                        media_content.document.save(pdf_path.name, File(pdf_file))
                    media_content.save()
                    exists_pdf = True
            except FileNotFoundError:
                continue
            if not exists_pdf:
                media.delete()

