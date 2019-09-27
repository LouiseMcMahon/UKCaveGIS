# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters  import JsonItemExporter
from scrapy.exceptions import DropItem
import simplekml
import re

class DataCleanup(object):
    def process_item(self, item, spider):
        try:
            if isinstance(item['wgS84'], str) and ',' in item['wgS84']:
                 item['wgS84'] = item['wgS84'].split(',')

            if not isinstance(item['wgS84'], list) or len(item['wgS84']) != 2:
                raise DropItem('Failed to convert wgS84' % item)
        except:
            raise DropItem('Failed to convert wgS84' % item)

        if isinstance(item['tags'], str):
             item['tags'] = item['tags'].split(',')

        item['altitude'] = self.convert_string_to_int(item['altitude'])
        item['depth'] = self.convert_string_to_int(item['depth'])
        item['length'] = self.convert_string_to_int(item['length'])

        return item

    def convert_string_to_int(self, string):
        try:
            string = re.sub('[^0-9]','', string)
            string = int(string)
        except:
            return None

        return string

class KMLPipeline(object):
    documents = {}
    unsaved_count = {}

    def open_spider(self, spider):
        kml = simplekml.Kml()
        kml.document.name = spider.registry + ' caves and mines'
        self.documents[spider.registry] = kml
        self.unsaved_count[spider.registry] = 0

    def close_spider(self, spider):
        self.documents[spider.registry].save('data/' + spider.registry + '.kml')

    def process_item(self, item, spider):
        item_cordinates = None
        if item['altitude'] is not None and item['altitude'] > 0:
            item_cordinates = [(item['wgS84'][0], item['wgS84'][1], str(item['altitude']))]
        else:
            item_cordinates = [(item['wgS84'][0], item['wgS84'][1])]

        self.documents[spider.registry].newpoint(name=item['name'], coords=item_cordinates)

        self.unsaved_count[spider.registry] += 1
        if(self.unsaved_count[spider.registry] > 10):
            self.unsaved_count[spider.registry] = 0
            self.documents[spider.registry].save('data/' + spider.registry + '.kml')

        return item

class GPXPipeline(object):
    pass

class JsonPipeline(object):
    files = {}
    exporters = {}

    def open_spider(self, spider):
        self.files[spider.registry] = open('data/' + spider.registry + '.json', 'wb')
        self.exporters[spider.registry] = JsonItemExporter(self.files[spider.registry], encoding='utf-8', ensure_ascii=False)
        self.exporters[spider.registry].start_exporting()

    def close_spider(self, spider):
        self.exporters[spider.registry].finish_exporting()
        self.files[spider.registry].close()

    def process_item(self, item, spider):
        self.exporters[spider.registry].export_item(item)
        return item
