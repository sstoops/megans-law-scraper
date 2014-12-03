# -*- coding: utf-8 -*-
import re
import time
from urlparse import parse_qs

from dateutil.parser import parse as date_parse
import scrapy
from scrapy import log
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from sexoff_scraper.items import SexoffScraperItem


ID_RE = re.compile(r'.*\(\'(\w+)\'\)$')


class SexoffSpider(scrapy.Spider):
    name = "sexoff"
    allowed_domains = ["www.meganslaw.ca.gov"]
    start_urls = (
        'http://www.meganslaw.ca.gov/cgi/prosoma.dll?searchby=curno',
    )
    pagination_url = "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=%s&searchby=CountyList&SelectCounty=ORANGE&SB=0&PageNo=%s"
    profile_url = "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=%s&searchby=offender&id=%s"
    session_id = None
    pages = None

    def parse_first_page(self, response):
        sel = Selector(response)
        self.pages = int(sel.xpath(
            '((//td[@align="right" and @valign="top"])[1]/a)[last()]/text()'
            ).extract()[0].strip())

        # Unroll the first page's requests
        for req in self.parse_page(response):
            yield req

        # Make the rest of the pagination requests
        for x in xrange(1, self.pages + 1):
            self.log('Requesting page: %s' % x, level=log.INFO)
            yield Request(
                self.pagination_url % (self.session_id, x),
                callback=self.parse_page)

    def parse_page(self, response):
        self.log('Processing page of results', level=log.INFO)
        self.log(response.url)
        sel = Selector(response)
        hrefs = sel.xpath(
            '(//table[@id="table14"]//table)[1]//tr[position()>1]/td[1]/a/@href'
            ).extract()
        ids = map(lambda x:ID_RE.findall(x)[0], hrefs)
        self.log('Profile IDs: %s' % str(ids))
        for x in ids:
            self.log('Requesting profile: %s' % x, level=log.INFO)
            yield Request(
                self.profile_url % (self.session_id, x),
                self.parse_profile)

    def parse_profile(self, response):
        self.log('Processing profile')
        self.log(response.url)
        sel = Selector(response)
        item = SexoffScraperItem()
        item['last_name'] = sel.xpath(
            '//div[@class="row"]/p[1]/text()').extract()[0].strip()
        item['first_name'] = sel.xpath(
            '//div[@class="row"]/p[2]/text()').extract()[0].strip()
        item['middle_name'] = sel.xpath(
            '//div[@class="row"]/p[3]/text()').extract()[0].strip()
        item['dob'] = date_parse(sel.xpath(
            '//td[@headers="dobColHdr"]/text()').extract()[0])
        item['gender'] = sel.xpath(
            '//td[@headers="genderColHdr"]/text()').extract()[0].strip()
        item['height'] = sel.xpath(
            '//td[@headers="heigthColHdr"]/text()').extract()[0].strip()
        item['weight'] = sel.xpath(
            '//td[@headers="weigthColHdr"]/text()').extract()[0].strip()
        item['eye_color'] = sel.xpath(
            '//td[@headers="eyecolorColHdr"]/text()').extract()[0].strip()
        item['hair_color'] = sel.xpath(
            '//td[@headers="haircolorColHdr"]/text()').extract()[0].strip()
        item['ethnicity'] = sel.xpath(
            '//td[@headers="ethnicityColHdr"]/text()').extract()[0].strip()
        item['address'] = sel.xpath(
            '//td[@headers="lastKnwnAddrColHdr"]/text()').extract()[0].strip()
        return item

    def parse(self, response):
        self.log('Fetching session data', level=log.INFO)
        self.session_id = response.body.strip()
        self.log('SESSION ID: %s' % self.session_id, level=log.INFO)
        self.log('Requesting first page', level=log.INFO)
        yield Request(
            self.pagination_url % (self.session_id, 1),
            callback=self.parse_first_page)

        
