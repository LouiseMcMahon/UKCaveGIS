# -*- coding: utf-8 -*-
import scrapy
import logging
from ukcavegis.utils import extract_with_css, extract_with_xpath
from ukcavegis.items import Entry

class CccRegistry(scrapy.Spider):
    name = 'cccregistry'
    allowed_domains = ['cambriancavingcouncil.org.uk']
    start_urls = ['http://www.cambriancavingcouncil.org.uk/registry/ccr_registry.php?reg=All+Wales+and+the+Marches&nam=']
    registry = 'WalesAndMarches'

    def parse(self, response):
        # follow links to cave pages
        for link in response.xpath('/html/body/table//a'):
            yield response.follow(link, self.parse_cave)

    def parse_cave(self, response):
        entry = Entry()

        entry['name'] = extract_with_css(response, '.Heading1::text')
        entry['ngr'] = extract_with_xpath(response, '/html/body/table/tr[1]/td[2]/text()[3]').replace('NGR: ','').replace('\xa0',' ').strip()
        entry['length'] = extract_with_xpath(response, '/html/body/table/tr[1]/td[1]/text()[2]').replace('L:','').strip()
        entry['depth'] = extract_with_xpath(response, '/html/body/table/tr[1]/td[1]/text()[3]').replace('V:','').strip()
        entry['altitude'] = extract_with_xpath(response, '/html/body/table/tr[1]/td[2]/text()[4]').replace('m.asl', '').strip()
        entry['registry'] = self.registry

        yield entry

    def split_colon_value(self, value):
        return_value = value.split(':')
