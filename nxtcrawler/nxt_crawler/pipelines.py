import json
import requests
import datetime as dt
import traceback

from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.settings import Settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from nxt_crawler.database.models import Gazette, initialize_database


class GazetteDateFilteringPipeline:
    def process_item(self, item, spider):
        if hasattr(spider, "start_date"):
            if spider.start_date > item.get("date"):
                raise DropItem("Droping all items before {}".format(spider.start_date))
        return item


class DefaultValuesPipeline:
    """Add defaults values field, if not already set in the item"""

    default_field_values = {
        "territory_id": lambda spider: getattr(spider, "TERRITORY_ID"),
        "scraped_at": lambda spider: dt.datetime.utcnow(),
    }

    def process_item(self, item, spider):
        for field in self.default_field_values:
            if field not in item:
                item[field] = self.default_field_values.get(field)(spider)
        return item


class SQLDatabasePipeline:
    def __init__(self, database_url):
        self.database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("QUERIDODIARIO_DATABASE_URL")
        return cls(database_url=database_url)

    def open_spider(self, spider):
        if self.database_url is not None:
            engine = initialize_database(self.database_url)
            self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if self.database_url is None:
            return item

        session = self.Session()

        fields = [
            "source_text",
            "date",
            "edition_number",
            "is_extra_edition",
            "power",
            "scraped_at",
            "territory_id",
        ]
        gazette_item = {field: item.get(field) for field in fields}

        for file_info in item.get("files", []):
            already_downloaded = file_info["status"] == "uptodate"
            if already_downloaded:
                # We should not insert in database information of
                # files that were already downloaded before
                continue

            gazette_item["file_path"] = file_info["path"]
            gazette_item["file_url"] = file_info["url"]
            gazette_item["file_checksum"] = file_info["checksum"]

            gazette = Gazette(**gazette_item)
            session.add(gazette)
            try:
                session.commit()
            except SQLAlchemyError as exc:
                spider.logger.warning(
                    f"Something wrong has happened when adding the gazette in the database."
                    f"Date: {gazette_item['date']}. "
                    f"File Checksum: {gazette_item['file_checksum']}.",
                    f"Details: {exc.args}",
                )
                session.rollback()
            else:
                session.close()

        return item


class QueridoDiarioFilesPipeline(FilesPipeline):
    """Pipeline to download files described in file_urls or file_requests item fields.

    The main differences from the default FilesPipelines is that this pipeline:
        - organizes downloaded files differently (based on territory_id)
        - adds the file_requests item field to download files from request instances
        - allows a download_file_headers spider attribute to modify file_urls requests
    """

    DEFAULT_FILES_REQUESTS_FIELD = "file_requests"

    def __init__(self, *args, settings=None, **kwargs):
        super().__init__(*args, settings=settings, **kwargs)

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.files_requests_field = settings.get(
            "FILES_REQUESTS_FIELD", self.DEFAULT_FILES_REQUESTS_FIELD
        )

    def get_media_requests(self, item, info):
        """Makes requests from urls and/or lets through ready requests."""
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        download_file_headers = getattr(info.spider, "download_file_headers", {})
        yield from (Request(u, headers=download_file_headers) for u in urls)

        requests = ItemAdapter(item).get(self.files_requests_field, [])
        yield from requests

    def item_completed(self, results, item, info):
        """
        Transforms requests into strings if any present.
        Default behavior also adds results to item.
        """
        requests = ItemAdapter(item).get(self.files_requests_field, [])
        if requests:
            ItemAdapter(item)[self.files_requests_field] = [
                f"{r.method} {r.url}" for r in requests
            ]

        return super().item_completed(results, item, info)

    def file_path(self, request, response=None, info=None, item=None):
        """
        Path to save the files, modified to organize the gazettes in directories.
        The files will be under <territory_id>/<gazette date>/.
        """

        filepath = super().file_path(request, response=response, info=info, item=item)
        # The default path from the scrapy class begins with "full/". In this
        # class we replace that with the territory_id and gazette date.
        datestr = item["date"].strftime("%Y-%m-%d")
        filename = Path(filepath).name
        return str(Path(item["territory_id"], datestr, filename))


class NewsPipeline(object):

    def __init__(self, nxt_token, nxt_api_url):
        self.headers = {
            'Authorization': f'Token {nxt_token}',
            'Content-Type': 'application/json',
        }
        self.nxt_api_url = nxt_api_url

    @classmethod
    def from_crawler(cls, crawler):
        nxt_token = crawler.settings.get("NXT_TOKEN")
        nxt_api_url = crawler.settings.get("NXT_API_URL")
        return cls(nxt_token=nxt_token, nxt_api_url=nxt_api_url)

    def open_spider(self, spider):
        url = f'{self.nxt_api_url}api/execution/'
        data = {
            'crawler': spider.name,
            'status': 'created',
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            spider.log('-----------CRAWLER-----------')
            spider.nxt_crawler = response.json()
        except:
            traceback.print_exc()

    def close_spider(self, spider):
        spider.log(spider.nxt_crawler)
        if spider.nxt_crawler is not None:
            url = f'{self.nxt_api_url}api/execution/{spider.nxt_crawler["id"]}/'
            log = spider.crawler.stats.get_stats()
            def convert(o):
                if isinstance(o, dt.datetime):
                    return str(o)
            log = json.dumps(log, default=convert)
            data = {
                'status': 'finished',
                'finish': dt.datetime.now().isoformat(),
                'log': log,
            }
            try:
                response = requests.patch(url, json=data, headers=self.headers)
                spider.log(response.text)
            except:
                traceback.print_exc()

    def process_item(self, item, spider):
        publish_date_raw = item.get('publish_date_raw', '')
        data = {
            'title': item.get('title', ''),
            'url': item.get('url', ''),
            'source': item['source'],
            'publish_date_raw': publish_date_raw.strip(),
            'resume': item.get('resume', ''),
            'authors': item.get('authors', ''),
            'image': item.get('image', ''),
            'editorial': item.get('editorial'),
            'publish_date': item['publish_date'].isoformat(),
        }
        url = f'{self.nxt_api_url}api/media/'
        response = requests.post(url, json=data, headers=self.headers)
        spider.log(response.json())
        try:
            media_id = response.json()['id']
            data = {
                'media': media_id,
                'transcription': item.get('content', ''),
                'order': 1,
                'processed': True,
            }
            url = f'{self.nxt_api_url}api/media-content/'
            r = requests.post(url, json=data, headers=self.headers)
            spider.log(r.status_code)
        except Exception as ex:
            spider.log("--------------ERRROOORRRR-------------")
        return item
