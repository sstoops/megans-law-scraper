# -*- coding: utf-8 -*-
# import shelve
# from twisted.persisted import dirdbm as shelve
from geopy.geocoders import GoogleV3
from scrapy import log


class GeocoderPipeline(object):

    def __init__(self):
        log.msg('Initializing geocoder pipeline')
        self.geocoder = GoogleV3()
        self.geocoder_cache = {}

    def process_item(self, item, spider):
        address = item['address'] or ''
        if not address or address == 'ABSCONDED':
            log.msg('Item has no address, skip geocode', level=log.WARNING)
            return item
        log.msg('Geocoding address: "%s"' % address)

        if self.geocoder_cache.has_key(str(address)):
            log.msg('Geolocation found in cache, using')
            loc = self.geocoder_cache.get(str(address))
        else:
            try:
                geo_response = self.geocoder.geocode(address)
                log.msg('Location found')
                log.msg(str(geo_response), level=log.DEBUG)
                loc = {
                    'address': geo_response.address,
                    'latitude': geo_response.latitude,
                    'longitude': geo_response.longitude
                }
            except:
                log.msg('GEOCODING ERROR', level=log.ERROR)
                return item
        item['address'] = loc['address']
        item['lat'] = loc['latitude']
        item['lng'] = loc['longitude']
        log.msg('Writing geolocation object to cache')
        log.msg(str(loc), level=log.DEBUG)
        self.geocoder_cache[str(address)] = loc
        # self.geocoder_cache.sync()
        return item
