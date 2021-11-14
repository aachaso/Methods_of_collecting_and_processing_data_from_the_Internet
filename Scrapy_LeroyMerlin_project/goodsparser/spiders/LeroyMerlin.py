import scrapy
from scrapy.http import HtmlResponse
from goodsparser.items import GoodsParserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'LeroyMerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.good_parse)
        print()

    def good_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=GoodsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('price_fract', "//span[@slot='fract']/text()")
        loader.add_xpath('photos', "//source[@media='(max-width: 767px)']/@srcset")
        loader.add_value('url', response.url)
        loader.add_xpath('term', "//div[@class='def-list__group']/dt[@class='def-list__term']/text()")
        loader.add_xpath('definition', "//div[@class='def-list__group']/dd[@class='def-list__definition']/text()")
        yield loader.load_item()

        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@slot='price']/text()").get()
        # price_fract = response.xpath("//span[@slot='fract']/text()").get()
        # photos = response.xpath("//source[@media='(max-width: 767px)']/@srcset").getall()
        # url = response.url
        # yield GoodsparserItem(url=url, name=name, price=price, price_fract=price_fract, photos=photos)