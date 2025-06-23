import datetime as dt
import scrapy

from dateutil.rrule import DAILY, rrule

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class PbJoaoPessoaSpider(BaseGazetteSpider):
    name = "pb_joao_pessoa"
    TERRITORY_ID = "2507507"
    start_date = dt.date(2022, 3, 28)
    start_urls = ["https://www.joaopessoa.pb.gov.br/doe-jp/"]

    def parse(self, response):
        follow_next_page = True

        gazettes = response.css("h4.card-title")
        for gazette in gazettes:
            gazette_url = gazette.xpath(".//following-sibling::a/@href").get()
            edition_number = gazette.css("a::text").re_first(r"Edição (\d+\/\d+)")

            raw_gazette_date = gazette.css("a::text").re_first(r"(\d{2}\/\d{2}\/\d{4})")
            if not raw_gazette_date:
                continue

            gazette_date = dt.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                power="executive_legislative",
            )

            if gazette_date < self.start_date:
                follow_next_page = False
                break

        next_page_url = response.css("a.next::attr(href)").get()
        if follow_next_page and next_page_url:
            yield scrapy.Request(next_page_url)


class PbUFSpider(BaseGazetteSpider):

    name = "pb_uf"
    TERRITORY_ID = "25"
    start_date = dt.date(2022, 8, 1)
    allowed_domains = ["auniao.pb.gov.br"]
    BASE_URL = "https://auniao.pb.gov.br/doe"
    start_urls = [BASE_URL]

    def parse(self, response):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%d-%m-%Y')
            months = {
                1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
                5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
                9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro',
            }
            month = months[date.month]
            base_url = 'https://auniao.pb.gov.br/servicos/doe/'
            file_url = f'{base_url}{date.year}/{month}/diario-oficial-{date_str}.pdf'
            yield Gazette(
                date=date.date(),
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive_legislative",
            )
