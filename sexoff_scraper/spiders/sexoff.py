# -*- coding: utf-8 -*-
import re
import time
from urlparse import parse_qs

from dateutil.parser import parse as date_parse
import scrapy
from scrapy import log
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.by import By

from sexoff_scraper.items import SexoffScraperItem


class SexoffSpider(scrapy.Spider):
    name = "sexoff"
    allowed_domains = ["www.meganslaw.ca.gov"]
    start_urls = (
        'http://www.meganslaw.ca.gov/disclaimer.aspx?lang=ENGLISH',
    )
    pagination_url = "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=%s&searchby=CountyList&SelectCounty=ORANGE&SB=0&PageNo=%s"
    profile_url = "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=%s&searchby=offender&id=%s"
    session_id = None
    pages = None
    id_re = re.compile(r'.*\(\'(\w+)\'\)$')

    def parse_page(self, response):
        self.log('Processing page of results', level=log.INFO)
        self.log(response.url)
        sel = Selector(response)
        hrefs = sel.xpath(
            '(//table[@id="table14"]//table)[1]//tr[position()>1]/td[1]/a/@href'
            ).extract()
        ids = map(lambda x:self.id_re.findall(x)[0], hrefs)
        self.log('Profile IDs:', str(ids))
        for x in ids:
            self.log('Requesting profile:', x, level=log.INFO)
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

    def login(self):
        self.log('Logging into the Megan\'s Law system with Selenium', level=log.INFO)
        self.log('Loading disclaimer', level=log.INFO)
        driver = webdriver.Chrome()
        driver.get('http://www.meganslaw.ca.gov/disclaimer.aspx?lang=ENGLISH')
        time.sleep(2)
        self.log('Accepting disclaimer', level=log.INFO)
        driver.find_element(By.NAME, 'cbAgree').click()
        driver.find_element(By.ID, 'B1').click()
        self.log('Loading search by Orange County', level=log.INFO)
        driver.get(
            'http://www.meganslaw.ca.gov/search_main.aspx?\
            searchBy=county&county=orange&lang=ENGLISH')
        time.sleep(2)
        self.log('Loading list view', level=log.INFO)
        driver.execute_script('ViewList("countylist")')
        time.sleep(3)
        self.log('Scraping session data:', level=log.INFO)
        url = driver.current_url
        self.pages = int(driver.find_element(
            By.XPATH,
            '((//td[@align="right" and @valign="top"])[1]/a)[last()]'
            ).text.strip())
        self.session_id = parse_qs(url)['W6'][0].strip()
        self.log('SESSION ID:', self.session_id, level=log.INFO)
        self.log('PAGE COUNT:', self.pages, level=log.INFO)
        driver.quit()
        self.log('Quitting Selenium', level=log.INFO)

    def parse(self, response):
        # First page
        self.login()
        for x in xrange(1, self.pages + 1):
            self.log('Requesting page: %s' % x, level=log.INFO)
            yield Request(
                self.pagination_url % (self.session_id, x),
                callback=self.parse_page)
