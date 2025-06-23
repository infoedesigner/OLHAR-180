import re
import datetime

import scrapy

from dateutil.rrule import DAILY, rrule

from dateparser import parse

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class GoGoianiaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5208707"
    name = "go_goiania"
    allowed_domains = ["goiania.go.gov.br"]
    start_urls = ["http://www4.goiania.go.gov.br/portal/site.asp?s=775&m=2075"]
    start_date = datetime.date(1960, 4, 21)

    def start_requests(self):
        initial_year = self.start_date.year
        end_year = datetime.date.today().year
        for year in range(initial_year, end_year + 1):
            yield scrapy.Request(
                f"http://www.goiania.go.gov.br/shtml//portal/casacivil/lista_diarios.asp?ano={year}"
            )

    def parse(self, response):
        gazettes = response.css("a")
        for gazette in gazettes:
            gazette_info = gazette.css("::text").re(
                r"Edi..o\s*n.\s*(\d+) de (\d{2}) de (.*?) de (\d{4})"
            )
            if not gazette_info:
                self.logger.warning(
                    f"Unable to identify gazette info for {response.url}."
                )
                continue

            edition_number, day, month, year = gazette_info
            gazette_date = parse(f"{day} de {month} de {year}", languages=["pt"]).date()
            if gazette_date < self.start_date:
                continue

            gazette_url = response.urljoin(gazette.css("::attr(href)").get())

            link_text = gazette.css("::text").get().lower()
            is_extra_edition = bool(
                re.search(r"suplemento|complemento|especial", link_text)
            )

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )

class GoUFSpider(BaseGazetteSpider):
    TERRITORY_ID = "52"
    name = "go_uf"
    allowed_domains = ["diariooficial.abc.go.gov.br"]
    start_urls = ["https://diariooficial.abc.go.gov.br/portal/visualizacoes/diario_oficial"]
    BASE_URL = "https://diariooficial.abc.go.gov.br/"

    def parse(self, response):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%Y-%m-%d')
            base_url = 'https://diariooficial.abc.go.gov.br/'
            api_url = f'{base_url}apifront/portal/edicoes/edicoes_from_data/{date_str}.json'
            yield scrapy.Request(
                api_url, callback=self.parse_api, meta={'date': date}
            )

    def parse_api(self, response):
        data = response.json()
        if not data['erro']:
            for item in data['itens']:
                file_url = f'https://diariooficial.abc.go.gov.br/portal/edicoes/download/{item["id"]}'
                yield Gazette(
                    date=response.meta['date'].date(),
                    file_urls=[file_url],
                    is_extra_edition=False,
                    power="executive",
                )
