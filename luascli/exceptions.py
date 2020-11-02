# -*- coding: utf-8 -*-
class LuasLineNotFound(Exception):
    pass


class LuasStopNotFound(Exception):
    def __init__(self, stop=""):
        self.stop = stop


class AddressLocationNotFound(Exception):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class LuasStopsNotOnSameLine(Exception):
    def __init__(self, first_stop="", second_stop=""):
        self.first_stop = first_stop
        self.second_stop = second_stop
