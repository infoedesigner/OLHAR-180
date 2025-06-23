import json

from django.conf import settings

from nxt.media.models import Source


def load_gazette(company):
    gazette_path = settings.BASE_DIR / 'nxt/media/fixtures/gazette.json'
    with open(gazette_path, 'r') as gazette_file:
        content = gazette_file.read()
        data = json.loads(content)
    for source in data:
        if Source.objects.filter(company=company, territory_id=source['territory_id']).exists():
            continue
        source['company'] = company
        Source.objects.create(**source)
