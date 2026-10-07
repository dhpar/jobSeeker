"""Run MySpider once in a fresh process.

A separate process gets its own Twisted reactor (the reactor cannot restart
inside the API server) and runs in the main thread, so signal handlers install
cleanly. Invoked as: python -m app.spiders.run_once (cwd must be backend/).
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.spiders.spider import MySpider

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MySpider)
    process.start()

if __name__ == "__main__":
    main()
