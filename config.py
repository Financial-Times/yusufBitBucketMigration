import ConfigParser
import requests
import json
import os



class DataLoader(ConfigParser.ConfigParser):

    def map_parser(self):
        config_headers = dict(self._sections)
        for k in config_headers:
            config_headers[k] = dict(self._defaults, **config_headers[k])
            config_headers[k].pop('__name__', None)
        return config_headers


    def dataload(self, filename):
        #config = ConfigParser.ConfigParser()
        self.optionxform = str
        self.read(filename)
        return self.map_parser()




