#!/usr/bin/python3.6

import json
import requests


class LibraryInfoGetter():


    def __init__(self, api_key, platform, name):
        self.__url = "https://libraries.io/api/%s/%s?api_key=%s" % (platform, name, api_key)


    def get(self):
        library_info = None
        try:
            response = requests.get(self.__url)
            if response.status_code == 200:
                library_info = json.loads(response.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            pass
        return library_info
