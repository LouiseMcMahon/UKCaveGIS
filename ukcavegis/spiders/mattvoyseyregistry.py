# -*- coding: utf-8 -*-
import scrapy
import logging
from ukcavegis.items import Entry

class mattvoyseyregistry(scrapy.Spider):
    name = None
    allowed_domains = [None]
    start_urls = [None]

    def parse(self, response):
        # follow links to cave pages
        for href in response.css('.rowhover tr')[1:].css('a::attr(href)'):
            yield response.follow(href, self.parse_cave)

        # follow pagination links
        for href in response.xpath('/html/body/div/div/p[1]').css('a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_cave(self, response):
        def extract_with_css(query):
            return_value = response.css(query).extract_first()
            if (return_value):
                return return_value.strip()
            else:
                return None

        def extract_with_xpath(query):
            return_value = response.xpath(query).extract_first()
            if(return_value):
                return return_value.strip()
            else:
                return None

        def format_as_attr_name(string):
            return string.strip().lower().replace(" ", "").replace(":", "")

        entry = Entry()

        entry['name'] = extract_with_css('h1::text')
        entry['ngr'] = extract_with_xpath('/html/body/div[2]/table/tr[1]/td[2]/text()')
        entry['wgS84'] = extract_with_xpath('/html/body/div[2]/table/tr[2]/td[2]/text()')
        entry['length'] = extract_with_xpath('/html/body/div[2]/table/tr[3]/td[2]/text()')
        entry['depth'] = extract_with_xpath('/html/body/div[2]/table/tr[4]/td[2]/text()')
        entry['altitude'] = extract_with_xpath('/html/body/div[2]/table/tr[5]/td[2]/text()')
        entry['tags'] = extract_with_xpath('/html/body/div[2]/table/tr[6]/td[2]/text()')
        entry['registry'] = extract_with_xpath('/html/body/div[2]/table/tr[7]/td[2]/text()')

        yield entry
