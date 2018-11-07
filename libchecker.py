#!/usr/bin/python3.6

import os
import requests
from requests.exceptions import ConnectionError


class LibraryInfoGetter():

    def __init__(self, api_key, platform, name):
        self.__api_key = api_key
        self.__platform = platform
        self.__name = name

    def get(self):
        url = "https://libraries.io/api/%s/%s?api_key=%s" % (self.__platform, self.__name, self.__api_key)
        try:
            response = requests.get(url)
            library_info = response.content.decode("utf-8") if response.status_code == 200 else ""
        except ConnectionError:
            library_info = ""
        return library_info


def main():
    api_key = os.environ.get("LIBRARIESIO_API_KEY")
    platform = os.environ.get("LIBRARIES_PLATFORM")
    name = os.environ.get("LIBRARY_NAME")
    getter = LibraryInfoGetter(api_key, platform, name)
    print(getter.get())

if __name__ == "__main__":
    main()
