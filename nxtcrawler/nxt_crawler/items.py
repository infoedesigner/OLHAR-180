import scrapy

from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose, Join

from w3lib.html import remove_tags


class Gazette(scrapy.Item):
    source_text = scrapy.Field()
    date = scrapy.Field()
    edition_number = scrapy.Field()
    file_checksum = scrapy.Field()
    file_path = scrapy.Field()
    file_url = scrapy.Field()
    file_requests = scrapy.Field()
    is_extra_edition = scrapy.Field()
    territory_id = scrapy.Field()
    power = scrapy.Field()
    scraped_at = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()



class NewsLoader(ItemLoader):

    default_output_processor = TakeFirst()


class News(scrapy.Item):

    title = scrapy.Field()
    resume = scrapy.Field()
    authors = scrapy.Field()
    image = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    url = scrapy.Field()
    publish_date = scrapy.Field()
