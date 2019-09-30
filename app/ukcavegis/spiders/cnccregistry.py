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
        entry['ngr'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[1]/td[2]/text()')
        entry['wgS84'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[2]/td[2]/text()')
        entry['length'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[3]/td[2]/text()')
        entry['depth'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[4]/td[2]/text()')
        entry['altitude'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[5]/td[2]/text()')
        entry['tags'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[6]/td[2]/text()')
        entry['registry'] = self.registry

        yield entry
