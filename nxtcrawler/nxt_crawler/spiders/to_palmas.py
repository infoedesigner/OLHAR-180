import datetime
import scrapy

from urllib.parse import urlencode

from dateutil.rrule import DAILY, rrule

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class ToPalmasSpider(BaseGazetteSpider):
    TERRITORY_ID = "1721000"
    name = "to_palmas"
    allowed_domains = ["diariooficial.palmas.to.gov.br"]
    start_date = datetime.date(2010, 3, 22)  # First gazette available

    custom_settings = {
        "MEDIA_ALLOW_REDIRECTS": True,
    }

    def start_requests(self):
        dt_inicial = self.start_date.strftime("%d/%m/%Y")
        dt_final = self.end_date.strftime("%d/%m/%Y")

        url_params = {
            "opcao": "datas",
            "dt_inicial": dt_inicial,
            "dt_final": dt_final,
            "btn_search": "Search",
        }
        params = urlencode(url_params)
        url = f"http://diariooficial.palmas.to.gov.br/resultado-pesquisa/?{params}"
        yield scrapy.Request(url)

    def _get_date_from_parent_edition(self, response, gazette):
        parent_gazette_class_id = gazette.re_first(r"treegrid-parent-(\d+)")
        parent_gazette_class = f"treegrid-{parent_gazette_class_id}"
        main_edition_gazette = response.css(f".{parent_gazette_class}")
        return main_edition_gazette.xpath("./td[2]/text()").get()

    def parse(self, response):
        gazettes = response.css(".diario-resultado-pesquisa tbody tr")
        for gazette in gazettes:
            raw_gazette_date = gazette.xpath("./td[2]/text()").get()
            gazette_url = response.urljoin(gazette.css("a::attr(href)").get())

            is_extra_edition = bool(gazette.xpath(".//*[contains(., 'Suplemento')]"))
            if is_extra_edition:
                # Extra Editions doesn't have a date in its line. We need to get it from
                # the main edition of that day
                raw_gazette_date = self._get_date_from_parent_edition(response, gazette)

            gazette_date = datetime.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()

            item = Gazette(
                date=gazette_date,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )
            yield scrapy.Request(
                gazette_url,
                method="HEAD",
                callback=self.parse_pdf_url,
                cb_kwargs={"item": item},
            )

        next_pages_urls = response.css(".pagination a::attr(href)").getall()
        for next_page_url in next_pages_urls:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_pdf_url(self, response, item):
        gazette_pdf_url = response.url
        item = Gazette(**item)
        item["file_urls"] = [gazette_pdf_url]
        yield item


class ToPalmasSpider(BaseGazetteSpider):
    TERRITORY_ID = "17"
    name = "to_uf"
    allowed_domains = ["diariooficial.to.gov.br"]
    start_date = datetime.date(2010, 3, 22)

    custom_settings = {
        "MEDIA_ALLOW_REDIRECTS": True,
    }

    def start_requests(self):
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            date_str = date.strftime('%Y-%m-%d')
            url_params = {
                "por": "texto",
                "texto": "",
                "data-inicial": date_str,
                "data-final": date_str,
            }
            params = urlencode(url_params)
            url = f"https://diariooficial.to.gov.br/busca/?{params}"
            request = scrapy.Request(url)
            request.meta['date'] = date
            yield request
    
    def parse(self, response):
        file_url = response.xpath("//table//a/@href").extract_first()
        if file_url:
            date = response.meta['date']
            yield Gazette(
                date=date.date(),
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive_legislative",
            )
