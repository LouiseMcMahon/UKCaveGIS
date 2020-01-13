import scrapy
from scrapy.crawler import CrawlerProcess
from ukcavegis.spiders import dcaregistry, mendipregistry, scotlandregistry, cnccregistry, cccRegistry, fodccagRegistry, ducRegistry
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(dcaregistry.DcaRegistry)
process.crawl(mendipregistry.MendipRegistry)
process.crawl(scotlandregistry.ScotlandRegistry)
process.crawl(cnccregistry.CnccRegistry)
process.crawl(ducRegistry.DucRegistry)
process.crawl(fodccagRegistry.FodccagRegistry)
process.crawl(cccRegistry.CccRegistry)
process.start()
