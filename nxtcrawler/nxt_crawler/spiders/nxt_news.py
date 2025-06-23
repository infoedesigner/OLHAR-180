import scrapy
import datetime as dt

from dateutil.parser import parse

from scrapy_selenium import SeleniumRequest

from urllib.parse import urlparse

from nxt_crawler.settings import NXT_TOKEN, NXT_API_URL


class NXTNewsSpider(scrapy.Spider):

    name = "nxt_news"
    allowed_domains = []
    nxt_crawler = None
    source_id = None
    source = None
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'nxt_crawler.pipelines.NewsPipeline': 100,
        },
        'DOWNLOADER_CLIENTCONTEXTFACTORY': 'nxt_crawler.middlewares.LegacyConnectContextFactory',
    }

    def start_requests(self):
        if self.source:
            source_url = f'{NXT_API_URL}api/source/{self.source}/?format=json'
        else:
            source_url = f'{NXT_API_URL}api/source/?format=json&source_type=site&is_active=true'
        headers = {
            'Authorization': f'Token {NXT_TOKEN}',
        }
        yield scrapy.Request(source_url, headers=headers)

    def parse(self, response, **kwargs):
        data = response.json()
        if self.source:
            results = [data]
        else:
            results = data['results']
        for source in results:
            if source['url_root']:
                url = source['url_root']
                domain = urlparse(url).netloc
                self.allowed_domains.append(domain)
                self.log(url)
                request = SeleniumRequest(url=url, callback=self.parse_home_source)
                request.meta['source'] = source
                yield request
                for editorial in source['editorials']:
                    if editorial['use_configuration_source']:
                        continue
                    editorial_home = editorial['url']
                    domain = urlparse(editorial_home).netloc
                    self.allowed_domains.append(domain)
                    request = SeleniumRequest(url=editorial_home, callback=self.parse_home)
                    request.meta['editorial'] = editorial
                    request.meta['source'] = source
                    yield request

    def parse_home_source(self, response):
        source = response.meta['source']
        links = response.xpath(f"{source['url_xpath']}/@href").extract()
        self.log('---------------LINKS-----------------')
        self.log(links)
        for link in links:
            if not link:
                continue
            link = response.urljoin(link)
            if source['website'] in link:
                request = SeleniumRequest(url=link, callback=self.parse_media)
                request.meta['source'] = source
                yield request

    def parse_home(self, response):
        editorial = response.meta['editorial']
        source = response.meta['source']
        links = response.xpath(f"{editorial['url_xpath']}/@href").extract()
        self.log(editorial['url_xpath'])
        self.log(links)
        for link in links:
            if not link:
                continue
            link = response.urljoin(link)
            if source['website'] in link:
                request = SeleniumRequest(url=link, callback=self.parse_media)
                request.meta['editorial'] = editorial
                request.meta['source'] = source
                yield request

    def parse_media(self, response):
        editorial = response.meta.get('editorial')
        source = response.meta['source']
        if editorial:
            title = response.xpath(f"{editorial['title_xpath']}/text()").extract_first()
            authors = response.xpath(f"{editorial['author_xpath']}/text()").extract_first() or ''
            editorial_id = editorial['id']
            publish_date_raw = response.xpath(f"{editorial['date_xpath']}/text()").extract_first() or ''
            texts = response.xpath(editorial['text_xpath'])
        else:
            title = response.xpath(f"{source['title_xpath']}/text()").extract_first()
            authors = response.xpath(f"{source['author_xpath']}/text()").extract_first() or ''
            editorial_id = None
            publish_date_raw = response.xpath(f"{source['date_xpath']}/text()").extract_first() or ''
            texts = response.xpath(source['text_xpath'])
        if not authors:
            authors = response.xpath('//meta[contains(@name, "author")]/@property').extract_first() or ''
        if not title:
            title = response.xpath('//title/text()').extract_first() or ''
        try:
            meta = response.xpath('//meta[contains(@name, "created")]/@content').extract_first()
            if not meta:
                meta = response.xpath('//meta[contains(@name, "modified")]/@content').extract_first()
            if not meta:
                meta = response.xpath("//meta[contains(@name, 'time')]/@content").extract_first()
            publish_date = parse(meta)
        except:
            publish_date = dt.datetime.now()
        item = {
            'title': title,
            'resume': response.xpath("//meta[@name='description']/@content").extract_first() or '',
            'authors': authors,
            'editorial': editorial_id,
            'publish_date': publish_date,
            'publish_date_raw': publish_date_raw[:254],
            'url': response.url,
            'source': source['id'],
        }
        contents = []
        for text in texts:
            contents.extend(text.getall())
        item['content'] = ''.join(contents)
        yield item
