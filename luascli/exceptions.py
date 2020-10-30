# -*- coding: utf-8 -*-
class LuasLineNotFound(Exception):
    pass


class LuasStopNotFound(Exception):
    pass


class AddressLocationNotFound(Exception):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
