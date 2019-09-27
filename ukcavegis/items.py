# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Entry(scrapy.Item):
    tags = scrapy.Field()
    name = scrapy.Field()
    altitude = scrapy.Field()
    ngr = scrapy.Field()
    depth = scrapy.Field()
    length = scrapy.Field()
    registry = scrapy.Field()
    wgS84 = scrapy.Field()
