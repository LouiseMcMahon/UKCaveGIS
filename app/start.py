import scrapy
from scrapy.crawler import CrawlerProcess
from ukcavegis.spiders import dcaregistry, mendipregistry, scotlandregistry, cnccregistry
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(dcaregistry.DcaRegistry)
process.crawl(mendipregistry.MendipRegistry)
process.crawl(scotlandregistry.ScotlandRegistry)
process.crawl(cnccregistry.CnccRegistry)
process.start()
