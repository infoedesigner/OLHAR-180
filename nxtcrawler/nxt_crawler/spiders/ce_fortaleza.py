import dateparser
import w3lib.url

from datetime import datetime
from dateutil.rrule import DAILY, rrule

from scrapy import Request

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class CeFortalezaSpider(BaseGazetteSpider):
    GAZETTE_ELEMENT_CSS = ".diarios-oficiais .table-responsive tbody tr"
    DATE_CSS = "td:nth-child(2)::text"
    EXTRA_CSS = "td:nth-child(1)::text"
    NEXT_PAGE_CSS = "ul.pagination .page-link::attr(href)"

    TERRITORY_ID = "2304400"

    allowed_domains = ["apps.fortaleza.ce.gov.br"]
    name = "ce_fortaleza"

    def start_requests(self):
        base_url = "http://apps.fortaleza.ce.gov.br/diariooficial/?mes-diario=todos"

        for year in range(1952, datetime.now().year + 1):
            year_url = w3lib.url.add_or_replace_parameter(base_url, "ano-diario", year)
            yield Request(year_url)

    def parse(self, response):
        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = response.urljoin(element.css("a::attr(href)").extract_first())
            date = dateparser.parse(
                element.css(self.DATE_CSS).extract_first(""), languages=["pt"]
            ).date()
            # Extra edition is maked with a "s" on description. Example: Diário Oficial Nº 15923s
            extra_edition = element.css(self.EXTRA_CSS).extract_first("").endswith("s")

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=extra_edition,
                power="executive",
            )

        for page_number in response.css(self.NEXT_PAGE_CSS).re(r"#(\d)+"):
            next_url = w3lib.url.add_or_replace_parameter(
                response.url, "current", page_number
            )
            yield Request(next_url)


class CeUFSpider(BaseGazetteSpider):

    TERRITORY_ID = "23"
    allowed_domains = ["pesquisa.doe.seplag.ce.gov.br"]
    name = "ce_uf"

    def start_requests(self):
        base_url = "http://pesquisa.doe.seplag.ce.gov.br/doepesquisa/sead.do?page=ultimasDetalhe&cmd=10&action=Cadernos&data={}"

        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%Y%m%d')
            edition_url = base_url.format(date_str)
            request = Request(url=edition_url)
            request.meta['date'] = date
            yield request

    def parse(self, response):
        date = response.meta['date']
        for i, link in enumerate(response.xpath('//a/@href').extract()):
            yield Gazette(
                date=date.date(),
                file_urls=[response.url],
                is_extra_edition=False,
                power="executive",
            )
