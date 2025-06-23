import datetime as dt

import scrapy

from nxt_crawler.items import Gazette
from nxt_crawler.spiders.base import BaseGazetteSpider


class ApMacapaSpider(BaseGazetteSpider):

    name = "ap_macapa"
    allowed_domains = ["macapa.ap.gov.br"]
    start_date = None

    TERRITORY_ID = "1600303"

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        self.start_date = dt.date(2018, 1, 1)

        super(ApMacapaSpider, self).__init__(start_date, end_date)

        self.logger.debug(
            "Start date is {date}".format(date=self.start_date.isoformat())
        )
        self.logger.debug("End date is {date}".format(date=self.end_date.isoformat()))

    def start_requests(self):
        base_url = "https://macapa.ap.gov.br/"

        target_date = self.start_date
        data = {
            "s": "",
            "post_type": "official_diaries",
            "search": "official_diaries",
            "official_diary_number": "",
        }
        while target_date <= self.end_date:
            formatted_date = target_date.strftime("%d/%m/%Y")
            data.update(
                {
                    "official_diary_initial_date": formatted_date,
                    "official_diary_final_date": formatted_date,
                }
            )

            yield scrapy.FormRequest(
                url=base_url, formdata=data, method="GET", meta={"date": target_date}
            )
            target_date = target_date + dt.timedelta(days=1)

    def parse(self, response):
        # Extract Items
        links = response.xpath('//i[@class="fa fa-file-pdf-o"]/parent::a')
        links = links.xpath("@href").getall()

        gazette_date = response.meta["date"]

        if len(links) == 0:
            self.logger.warning(
                "No gazettes found for date {date}".format(date=gazette_date)
            )

        for index, file_url in enumerate(links):
            yield Gazette(
                date=gazette_date,
                file_urls=[file_url],
                is_extra_edition=(index > 0),
                power="executive_legislative",
            )


# class ApUFSpider(BaseGazetteSpider):

#     name = "ap_uf"
#     TERRITORY_ID = "16"
#     start_date = dt.date(2022, 8, 1)
#     allowed_domains = ["auniao.pb.gov.br"]
#     BASE_URL = "https://auniao.pb.gov.br/doe"
#     start_urls = [BASE_URL]

#     def parse(self, response):
#         for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
#             date_str = date.strftime('%d-%m-%Y')
#             months = {
#                 1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
#                 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
#                 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro',
#             }
#             month = months[date.month]
#             base_url = 'https://auniao.pb.gov.br/servicos/doe/'
#             file_url = f'{base_url}{date.year}/{month}/diario-oficial-{date_str}.pdf'
#             yield Gazette(
#                 date=date.date(),
#                 file_urls=[file_url],
#                 is_extra_edition=False,
#                 power="executive_legislative",
#             )

