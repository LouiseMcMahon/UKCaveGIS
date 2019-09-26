# -*- coding: utf-8 -*-
import scrapy
import logging

class DcaregistrySpider(scrapy.Spider):
    name = 'dcaRegistry'
    allowed_domains = ['registry.thedca.org.uk']
    start_urls = ['https://registry.thedca.org.uk/registry/browse.php']

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

        data = {
            'name': extract_with_css('h1::text'),
            'ngr': extract_with_xpath('/html/body/div[2]/table/tr[1]/td[2]/text()'),
            'wgS84': extract_with_xpath('/html/body/div[2]/table/tr[2]/td[2]/text()'),
            'length': extract_with_xpath('/html/body/div[2]/table/tr[3]/td[2]/text()'),
            'depth': extract_with_xpath('/html/body/div[2]/table/tr[4]/td[2]/text()'),
            'altitude': extract_with_xpath('/html/body/div[2]/table/tr[5]/td[2]/text()'),
            'tags': extract_with_xpath('/html/body/div[2]/table/tr[6]/td[2]/text()'),
            'registry': extract_with_xpath('/html/body/div[2]/table/tr[7]/td[2]/text()')
        }

        # get_data = False
        # el_clount = len(response.xpath('/html/body/*'))
        # i = -1
        # while el_clount > i:
        #     i += 1
        #     div = response.xpath('/html/body/*[' + str(i) + ']')
        #     logging.info(div)
        #     if div.xpath('/html/body/*[16]'):
        #         logging.info('in clear left')
        #         get_data = False
        #         data['resources'] = {}
        #         for resource in div.xpath('//ul/li'):
        #             data['resources'][format_as_attr_name(resource.css('///text()').extract_first())] = resource.css('a::attr(href)').extract_first()
        #         continue
        #
        #     if div.xpath('.//div[@id="markdown"]'):
        #         logging.info('in markdown')
        #         data['markdown'] = True
        #         get_data = True
        #         title = format_as_attr_name(div.xpath('//b/text()').extract_first())
        #         data[title] = div.xpath('//p/text()').extract_first()
        #         continue
        #
        #     if get_data:
        #         data[format_as_attr_name(div.xpath('//b/text()').extract_first())] = div.xpath('//text()').extract_first()
        #         pass

        yield data