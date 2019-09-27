import scrapy
from scrapy.crawler import CrawlerProcess
from ukcavegis.spiders import dcaregistry, mendipregistry, scotlandregistry
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(dcaregistry.DcaRegistry)
process.crawl(mendipregistry.MendipRegistry)
process.crawl(scotlandregistry.ScotlandRegistry)
process.start() # the script will block here until all crawling jobs are finished
