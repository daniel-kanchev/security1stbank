import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from security1stbank.items import Article


class security1stbankSpider(scrapy.Spider):
    name = 'security1stbank'
    start_urls = ['https://security1stbank.com/news-events/']

    def parse(self, response):
        links = response.xpath('//a[text()="Read Full Article"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@id="single_meta"]/text()').get()
        if date:
            date = " ".join(date.split()[2:5])

        content = response.xpath('//article//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
