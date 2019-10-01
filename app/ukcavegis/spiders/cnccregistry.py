# -*- coding: utf-8 -*-
import scrapy
import logging
from ukcavegis.utils import extract_with_css, extract_with_xpath
from ukcavegis.items import Entry

class CnccRegistry(scrapy.Spider):
    name = 'cnccregistry'
    allowed_domains = ['cncc.org.uk']
    start_urls = ['https://cncc.org.uk/caving/caves/postback.php']
    registry = 'Yorkshire'

    def parse(self, response):
        # follow links to cave pages
        for link in response.xpath('//a'):
            if '/cave/' in link.attrib['href']:
                yield response.follow(link, self.parse_cave)

        # follow pagination links
        for href in response.xpath('/html/body/div/div/p[1]').css('a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_cave(self, response):
        entry = Entry()

        entry['name'] = extract_with_css(response, 'h1::text')
        entry['registry'] = self.registry

        for p in response.xpath('//p/text()').getall():
            if 'NGR:' in p:
                entry['ngr'] = self.split_colon_value(p)

            if 'Lat/long:' in p:
                entry['wgS84'] = self.split_colon_value(p)

        yield entry

    def split_colon_value(self, value):
        return_value = value.split(':')
        return return_value[1].strip()
