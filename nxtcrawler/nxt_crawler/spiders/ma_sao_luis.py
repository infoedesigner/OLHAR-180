import scrapy
import datetime as dt

from dateutil.rrule import DAILY, rrule

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider

class MaSaoLuisSpider(BaseGazetteSpider):
    TERRITORY_ID = "2111300"
    name = "ma_sao_luis"
    allowed_domains = ["diariooficial.saoluis.ma.gov.br"]
    start_urls = ["https://diariooficial.saoluis.ma.gov.br/dom/dom/todasEdicoes/"]
    BASE_URL = "https://diariooficial.saoluis.ma.gov.br/dom/dom/todasEdicoes/"

    def parse(self, response):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            formdata = {
                'caxPesquisa': '',
                'caxDtInicio':date.strftime('%d/%m/%Y'),
                'caxDtFim': date.strftime('%d/%m/%Y'),
            }
            request = scrapy.FormRequest(
                url=self.BASE_URL, formdata=formdata,
                callback=self.parse_search
            )
            request.meta['date'] = date
            yield request

    def parse_search(self, response):
        url = 'https://diariooficial.saoluis.ma.gov.br/dom/dom/pesquisaEdicoes/'
        date = response.meta['date']
        request = scrapy.Request(url=url, callback=self.parse_item)
        request.meta['date'] = date
        yield request

    def parse_item(self, response):
        data = response.json()
        file_url = 'https://painel.siganet.net.br/upload/0000000485/cms/publicacoes/diario/{}'
        for item in data['data']:
            yield Gazette(
                date=response.meta['date'].date(),
                file_urls=[file_url.format(item['TDO_ASSINADO_ARQUIVO'])],
                is_extra_edition=False,
                power="executive",
            )
