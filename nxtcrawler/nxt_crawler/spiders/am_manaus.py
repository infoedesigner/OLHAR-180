import datetime as dt
import re

import scrapy

from dateutil.rrule import DAILY, rrule

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class AmManausSpider(BaseGazetteSpider):

    name = "am_manaus"
    allowed_domains = ["dom.manaus.am.gov.br"]
    start_date = dt.date(2000, 4, 3)
    start_urls = ["http://dom.manaus.am.gov.br/diario-oficial-de-manaus"]

    TERRITORY_ID = "1302603"

    def parse(self, response):
        follow_next_page = True
        gazettes = response.css(".listing tbody tr")
        for gazette in gazettes:
            gazette_date_raw = gazette.xpath("./td[1]//text()").re_first(
                r"\d{2}\/\d{2}\/\d{4}"
            )
            gazette_date = dt.datetime.strptime(
                gazette_date_raw, "%d/%m/%Y"
            ).date()

            if gazette_date < self.start_date:
                follow_next_page = False
                break

            title = "".join(gazette.xpath("./td[2]//text()").getall()).strip()
            edition_number = self._extract_edition_number(title, gazette_date)
            is_extra_edition = re.search(r"eex|ext", title.lower()) is not None
            gazette_url = gazette.css("a::attr(href)").get()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )

        if follow_next_page:
            next_page_url = response.css(".next a::attr(href)").get()
            yield scrapy.Request(next_page_url)

    def _extract_edition_number(self, text, gazette_date):
        year = gazette_date.year
        pattern = r"|".join(
            [
                r"Edição (\d+)\s",
                rf"dom{year}(\d{{4}})[A-Za-z.]",
                r"dom(\d{4})[A-Za-z.]",
                r"(\d+)\s",
            ]
        )
        matches = re.search(pattern, text)
        if matches:
            return matches.group(matches.lastindex)
        return ""

class AMUFSpider(BaseGazetteSpider):

    name = "am_uf"
    TERRITORY_ID = "13"
    start_date = dt.date(2022, 8, 1)
    allowed_domains = ["diario.imprensaoficial.am.gov.br"]
    BASE_URL = "https://diario.imprensaoficial.am.gov.br/"
    start_urls = [BASE_URL]

    def parse(self, response):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%Y-%m-%d')
            base_url = 'https://diario.imprensaoficial.am.gov.br/'
            api_url = f'{base_url}apifront/portal/edicoes/edicoes_from_data/{date_str}.json'
            yield scrapy.Request(
                api_url, callback=self.parse_api, meta={'date': date}
            )

    def parse_api(self, response):
        data = response.json()
        if not data['erro']:
            for item in data['itens']:
                file_url = f'https://diario.imprensaoficial.am.gov.br/portal/edicoes/download/{item["id"]}'
                yield Gazette(
                    date=response.meta['date'].date(),
                    file_urls=[file_url],
                    is_extra_edition=False,
                    power="executive_legislative",
                )
