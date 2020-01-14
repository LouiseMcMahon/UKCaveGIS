import scrapy
from scrapy.crawler import CrawlerProcess
from ukcavegis.spiders import dcaregistry, mendipregistry, scotlandregistry, cnccregistry, cccregistry, fodccagregistry, ducregistry
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(dcaregistry.DcaRegistry)
process.crawl(mendipregistry.MendipRegistry)
process.crawl(scotlandregistry.ScotlandRegistry)
process.crawl(cnccregistry.CnccRegistry)
process.crawl(ducregistry.DucRegistry)
process.crawl(fodccagregistry.FodccagRegistry)
process.crawl(cccregistry.CccRegistry)
process.start()
