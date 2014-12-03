# -*- coding: utf-8 -*-
from geopy.geocoders import GoogleV3
from scrapy import log


class GeocoderPipeline(object):

    def __init__(self):
        log.msg('Initializing geocoder pipeline')
        self.geocoder = GoogleV3()

    def process_item(self, item, spider):
        address = item['address']
        if not address:
            log.msg('Item has no address, skip geocode', level=log.WARNING)
            return item
        log.msg('Geocoding address: "%s"' % address)
        try:
            loc = self.geocoder.geocode(address)
            log.msg('Location found')
            log.msg(str(loc), level=log.DEBUG)
            item['address'] = loc.address
            item['lat'] = loc.latitude
            item['lng'] = loc.longitude
        except:
            log.msg('GEOCODING ERROR', level=log.ERROR)
            raise
        return item
