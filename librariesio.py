#!/usr/bin/python3.6

import requests


class LibraryInfoGetter():


    def __init__(self, api_key, platform, name):
        self.__url = "https://libraries.io/api/%s/%s?api_key=%s" % (platform, name, api_key)


    def get(self):
        try:
            response = requests.get(self.__url)
            library_info = response.content.decode("utf-8") if response.status_code == 200 else ""
        except requests.exceptions.ConnectionError:
            library_info = ""
        return library_info
