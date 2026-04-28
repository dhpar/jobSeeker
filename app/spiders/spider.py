import scrapy
import json

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4356531114&discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII' #
    ]
    # A place to store scraped data
    custom_settings = {
        'FEEDS': { 'output.json': {'format': 'json', 'overwrite': True}},
    }

    def parse(self, response):
        for quote in response.css('#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div.job-view-layout.jobs-details > div:nth-child(1) > div'):
            yield {
                'title': quote.css('div.relative.job-details-jobs-unified-top-card__container--two-pane > div:nth-child(1) > div.display-flex.justify-space-between.flex-wrap.mt2 > div > h1').get(),
                'text': quote.css('div.jobs-box--fadein.jobs-box--full-width.jobs-box--with-cta-large.jobs-description.jobs-description--reformatted.job-details-module > article > div').get()
            }