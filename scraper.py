"""Morph.io compatible script to run the main spider"""

import dblite
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from sexoff_scraper.spiders.sexoff import SexoffSpider

from scrapy.exceptions import DropItem
from sexoff_scraper.items import SexoffScraperItem

class StoreItemsPipeline(object):
    def __init__(self):
        self.ds = None

    def open_spider(self, spider):
        self.ds = dblite.open(SexoffScraperItem, 'sqlite://data.sqlite:data', autocommit=True)

    def close_spider(self, spider):
        self.ds.commit()
        self.ds.close()

    def process_item(self, item, spider):
        if isinstance(item, SexoffScraperItem):
            try:
                self.ds.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate item found: %s" % item)
        else:
            raise DropItem("Unknown item type, %s" % type(item))
        return item

def main():
    import sys
    sys.path.append("/home/scriptrunner/")
    spider = SexoffSpider(county='ORANGE')
    settings = get_project_settings()
    settings.set('ITEM_PIPELINES', {'scraper.StoreItemsPipeline': 1000})
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

if __name__ == '__main__':
    main()