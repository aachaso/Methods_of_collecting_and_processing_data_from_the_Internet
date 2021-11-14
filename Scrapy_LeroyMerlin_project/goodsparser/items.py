# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def change_price_type(value):
    try:
        value = value.replace(' ', '')
        value = int(value)
    except Exception as error:
        print(f'Ошибка при изменении типа! {error}')
    finally:
        return value

class GoodsParserItem(scrapy.Item):
    # define the fields for your item here like:

    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(change_price_type), output_processor=TakeFirst())
    price_fract = scrapy.Field(input_processor=MapCompose(change_price_type), output_processor=TakeFirst())
    term = scrapy.Field()
    definition = scrapy.Field()
    photos = scrapy.Field()
