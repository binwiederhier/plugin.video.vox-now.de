# -*- coding: utf-8 -*-

"""
Version 1.0.1 (2014.07.04)
- initial release
"""

__CONFIG_VOX_NOW__ = {'salt_phone': '9fb130b5-447e-4bbc-a44a-406f2d10d963',
                      'salt_tablet': '0df2738e-6fce-4c44-adaf-9981902de81b',
                      'key_phone': 'b11f23ac-10f1-4335-acb8-ebaaabdb8cde',
                      'key_tablet': '2e99d88e-088e-4108-a319-c94ba825fe29',
                      'url': 'www.voxnow.de',
                      'id': '41',
                      'http-header': {'X-App-Name': 'VOX NOW App',
                                      'X-Device-Type': 'voxnow_android',
                                      'X-App-Version': '1.3.1',
                                      'X-Device-Checksum': 'a5fabf8ef3f4425c0b8ff716562dd1a3',
                                      'Host': 'www.voxnow.de',
                                      'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'
                                      }
                      }

class Now:
    def __init__(self, config):
        self.Config = config
        
    def _getConnection(self):
        
        pass
    
    def _createQuery(self, params={}):
        
        pass
    
    def _request(self):
        pass
        
    def getShows(self):
        result = self._request('/api/query/json/content.list_formats')
        
        return result