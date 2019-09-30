# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters  import JsonItemExporter
from scrapy.exceptions import DropItem
from OSGridConverter import grid2latlong
from OSGridConverter import latlong2grid
import simplekml
import re
import gpxpy
import gpxpy.gpx


#Ensures all required fields are present and sets any empty or missing ones to None
class FieldCheck(object):
    def process_item(self, item, spider):
        if 'name' not in item.keys():
            raise DropItem('No name' % item)

        if 'registry' not in item.keys():
            raise DropItem('No registry set' % item)

        #2 letters + 10 numbers + 2 spaces = 14 char min for NGR
        if 'ngr' not in item.keys() or not isinstance(item['ngr'], str) or len(item['ngr']) < 14:
            item['ngr'] = None

        if 'wgS84' not in item.keys():
            item['wgS84'] = None

        if item['wgS84'] is None and item['ngr'] is None :
            raise DropItem('wgS84 and ngr not set' % item)

        if 'length' not in item.keys():
            item['length'] = None

        if 'depth' not in item.keys():
            item['depth'] = None

        if 'altitude' not in item.keys():
            item['altitude'] = None

        return item

# Converts fields to more usefull types
class TypeConversion(object):
    def process_item(self, item, spider):
        if isinstance(item['wgS84'], str) and ',' in item['wgS84']:
             item['wgS84'] = item['wgS84'].split(',')
             item['wgS84'][0] = float(item['wgS84'][0])
             item['wgS84'][1] = float(item['wgS84'][1])

        if not isinstance(item['wgS84'], list) or len(item['wgS84']) != 2:
            item['wgS84'] = None

        if item['wgS84'] is None and item['ngr'] is None:
            raise DropItem('wgS84 and ngr not set' % item)

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

# If ngr or wgS84 is missing this will attempt to generate one from the other
# The item will not reach this pipeline if both are missing
class GeoDataCheck(object):
    def process_item(self, item, spider):
        if item['wgS84'] is None:
            latlong = grid2latlong(item['ngr'], tag='WGS84')
            item['wgS84'] = [
                latlong.latitude,
                latlong.longitude
            ]

        if item['ngr'] is None:
            item['ngr'] = str(latlong2grid(item['wgS84'][0], item['wgS84'][1], tag='WGS84'))

        return item

# Generates a KML file for each region in the app/data folder
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

# Generates a GPX file for each region in the app/data folder
class GPXPipeline(object):
    documents = {}
    unsaved_count = {}

    def open_spider(self, spider):
        gpx = gpxpy.gpx.GPX()
        gpx.name = spider.registry + ' caves and mines'
        self.documents[spider.registry] = gpx
        self.unsaved_count[spider.registry] = 0

    def close_spider(self, spider):
        self.save_file(spider.registry)

    def process_item(self, item, spider):
        waypoint = gpxpy.gpx.GPXWaypoint(
            latitude=item['wgS84'][0],
            longitude=item['wgS84'][1],
            name=item['name']
        )

        if item['altitude'] is not None and item['altitude'] > 0:
            waypoint.elevation = item['altitude']

        self.documents[spider.registry].waypoints.append(waypoint)

        self.unsaved_count[spider.registry] += 1
        if(self.unsaved_count[spider.registry] > 10):
            self.unsaved_count[spider.registry] = 0
            self.save_file(spider.registry)

        return item

    def save_file(self, registry):
        xml = self.documents[registry].to_xml()
        f= open('data/' + registry + '.gpx', 'w+')
        f.seek(0)
        f.truncate()
        f.write(xml)
        f.close()

# Generates a JSON file for each region in the app/data folder
class JsonPipeline(object):
    files = {}
    exporters = {}

    def open_spider(self, spider):
        self.files[spider.registry] = open('data/' + spider.registry + '.json', 'w+')
        self.exporters[spider.registry] = JsonItemExporter(self.files[spider.registry], encoding='utf-8', ensure_ascii=False)
        self.exporters[spider.registry].start_exporting()

    def close_spider(self, spider):
        self.exporters[spider.registry].finish_exporting()
        self.files[spider.registry].close()

    def process_item(self, item, spider):
        self.exporters[spider.registry].export_item(item)
        return item
