import datetime as dt

import scrapy

from dateutil.rrule import DAILY, rrule

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class EsVitoriaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3205309"
    name = "es_vitoria"
    start_date = dt.date(2016, 7, 1)
    allowed_domains = ["diariooficial.vilavelha.es.gov.br"]

    BASE_URL = "https://diariooficial.vilavelha.es.gov.br/Default.aspx"


class EsUFSpider(BaseGazetteSpider):
    TERRITORY_ID = "32"
    name = "es_uf"
    allowed_domains = ["ioes.dio.es.gov.br"]
    start_urls = ["https://ioes.dio.es.gov.br/portal/visualizacoes/diario_oficial"]
    BASE_URL = "https://ioes.dio.es.gov.br/"

    def parse(self, response):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%Y-%m-%d')
            base_url = 'https://ioes.dio.es.gov.br/'
            api_url = f'{base_url}apifront/portal/edicoes/edicoes_from_data/{date_str}.json'
            yield scrapy.Request(
                api_url, callback=self.parse_api, meta={'date': date}
            )

    def parse_api(self, response):
        data = response.json()
        if not data['erro']:
            for item in data['itens']:
                file_url = f'https://ioes.dio.es.gov.br/portal/edicoes/download/{item["id"]}'
                yield Gazette(
                    date=response.meta['date'].date(),
                    file_urls=[file_url],
                    is_extra_edition=False,
                    power="executive",
                )
