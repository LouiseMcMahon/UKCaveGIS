# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters  import JsonItemExporter

class ukcavegisPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    files = {}
    exporters = {}

    def open_spider(self, spider):
        self.files[spider.registry] = open("data/" + spider.registry + ".json", 'wb')
        self.exporters[spider.registry] = JsonItemExporter(self.files[spider.registry], encoding='utf-8', ensure_ascii=False)
        self.exporters[spider.registry].start_exporting()

    def close_spider(self, spider):
        self.exporters[spider.registry].finish_exporting()
        self.files[spider.registry].close()

    def process_item(self, item, spider):
        self.exporters[spider.registry].export_item(item)
        return item
