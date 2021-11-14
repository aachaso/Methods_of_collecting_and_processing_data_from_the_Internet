# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
# from pymongo import MongoClient

class GoodsparserPipeline:

    # def __init__(self):
    #     client = MongoClient('localhost', 27017)
    #     self.mongo_base = client['Scrapy_spider_goods']


    def process_item(self, item, spider):

        goods_dict = {}
        goods_dict.update(item)

        if goods_dict.get('price_fract') == None:
            union_price = float(item['price'])
            goods_dict.update({'price': union_price})
        else:
            union_price = float(f'{item["price"]}.{item["price_fract"]}')
            goods_dict.update({'price': union_price})
            goods_dict.pop('price_fract')

        g_info = self.get_info_goods(goods_dict)
        goods_dict['info'] = g_info

        #
        # collection = self.mongo_base[spider.name]
        # collection.insert_one(goods_dict)

        return goods_dict

    def get_info_goods(self, goods):
        info = {}
        for t, d in zip(goods.get('term'), goods.get('definition')):
            goods_date = {}
            goods_date[t] = d.replace("\n", "").replace("  ", "")
            info.update(goods_date)

        goods.pop('term')
        goods.pop('definition')
        return info



class GoodsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as error:
                    print(f'Ошибка при обработке фото! {error}')

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item