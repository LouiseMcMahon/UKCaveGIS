# -*- coding: utf-8 -*-
import scrapy
import logging
from ukcavegis.items import Entry
from ukcavegis.utils import extract_with_css, extract_with_xpath

class MattVoyseyRegistry(scrapy.Spider):
    name = None
    allowed_domains = [None]
    start_urls = [None]
    registry = None

    def parse(self, response):
        # follow links to cave pages
        for href in response.css('.rowhover tr')[1:].css('a::attr(href)'):
            yield response.follow(href, self.parse_cave)

        # follow pagination links
        for href in response.xpath('/html/body/div/div/p[1]').css('a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_cave(self, response):        
        entry = Entry()

        entry['name'] = extract_with_css(response, 'h1::text')
        entry['ngr'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[1]/td[2]/text()')
        entry['wgS84'] = extract_with_xpath(response, '/html/body/div[2]/table/tr[2]/td[2]/text()')
        entry['registry'] = self.registry

        yield entry
