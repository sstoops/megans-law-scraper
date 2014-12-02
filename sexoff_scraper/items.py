# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SexoffScraperItem(scrapy.Item):
    last_name = scrapy.Field()
    first_name = scrapy.Field()
    middle_name = scrapy.Field()
    dob = scrapy.Field()
    gender = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    eye_color = scrapy.Field()
    hair_color = scrapy.Field()
    ethnicity = scrapy.Field()
    address = scrapy.Field()
