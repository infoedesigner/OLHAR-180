import re
import datetime

from urllib.parse import urlencode

from dateparser import parse
from dateutil.rrule import DAILY, rrule

from scrapy import Request

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class DfBrasiliaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5300108"
    name = "df_brasilia"
    start_date = datetime.date(1967, 12, 25)

    GAZETTE_URL = "https://dodf.df.gov.br/listar"
    DATE_REGEX = r"[0-9]{2}-[0-9]{2}[ -][0-9]{2,4}"
    EXTRA_EDITION_TEXT = "EDICAO EXTR"
    PDF_URL = "https://dodf.df.gov.br/index/visualizar-arquivo/?pasta={}&arquivo={}"

    def start_requests(self):
        """Requests page that has a list of all available years."""
        initial_year = self.start_date.year
        end_year = self.end_date.year
        for year in range(end_year, initial_year - 1, -1):
            yield Request(
                f"{self.GAZETTE_URL}?dir={year}",
                meta={"year": year},
                callback=self.parse_year,
            )

    def parse_year(self, response):
        """Parses available months to request list of available dates for each month."""
        months_available = response.json().get("data", [])
        year = response.meta["year"]

        for month in months_available:
            yield Request(
                f"{self.GAZETTE_URL}?dir={year}/{month}",
                meta={"month": month, "year": year},
                callback=self.parse_month,
            )

    def parse_month(self, response):
        """Parses available dates to request a list of documents for each date."""
        month, year = response.meta["month"], response.meta["year"]
        dates = response.json().get("data", [])

        for gazette_name in dates.values():
            date = re.search(self.DATE_REGEX, gazette_name).group()

            if date is None:
                continue

            date = parse(date, settings={"DATE_ORDER": "DMY"}).date()

            if date < self.start_date:
                continue

            url = f"{self.GAZETTE_URL}?dir={year}/{month}/{gazette_name}"
            yield Request(url, callback=self.parse_gazette)

    def parse_gazette(self, response):
        """Parses list of documents to request each one for the date."""
        json_response = response.json()
        if not json_response:
            self.logger.warning(f"Document not found in {response.url}")
            return

        json_dir = json_response["dir"]

        date = re.search(self.DATE_REGEX, json_dir).group()
        date = parse(date, settings={"DATE_ORDER": "DMY"}).date()
        is_extra_edition = self.EXTRA_EDITION_TEXT in json_dir
        path = json_dir.replace("/", "|")

        json_data = json_response["data"]
        file_urls = [self.PDF_URL.format(path, url.split("/")[-1]) for url in json_data]

        yield Gazette(
            date=date,
            file_urls=file_urls,
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )


class DfUFSpider(BaseGazetteSpider):

    TERRITORY_ID = "53"
    name = "df_uf"
    months = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
    }

    def start_requests(self):
        base_url = (
            'https://www.dodf.df.gov.br/listar?dir={}/{}_{}'
        )
        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            month = self.months[date.month]
            month_number = f'{date.month:02d}'
            month_url = base_url.format(date.year, month_number, month)
            request = Request(url=month_url, method='POST', dont_filter=True)
            request.meta['date'] = date
            yield request

    def parse(self, response):
        data = response.json()
        data = data['data']
        if data:
            date = response.meta['date']
            date_str = date.strftime('%Y%m%d')
            base_url = 'https://www.dodf.df.gov.br/listar?{}'
            month = self.months[date.month]
            month_number = f'{date.month:02d}'
            for key, value in data.items():
                if key.startswith(date_str):
                    folder = f'{date.year}/{month_number}_{month}/{value}'
                    params = {
                        'dir': folder
                    }
                    params = urlencode(params)
                    request = Request(
                        url=base_url.format(params), method='POST', dont_filter=True, callback=self.parse_item,
                    )
                    request.meta['date'] = date
                    request.meta['folder'] = folder
                    yield request

    def parse_item(self, response):
        data = response.json()
        folder = response.meta['folder']
        date = response.meta['date']
        self.log('---------------------')
        self.log(data['data'])
        for pdf in data['data']:
            file = pdf.split('/')[-1]
            file_url = f'https://www.dodf.df.gov.br/index/visualizar-arquivo/?pasta={folder}|&arquivo={file}'
            yield Gazette(
                date=date.date(),
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive",
            )
