#!/usr/bin/python3.6

import json
import requests


class LibraryInfoGetter():
    """
    Class responsible for consuming the Libraries.io API.
    """


    def __init__(self, api_key, platform, name):
        """
        The class requires an API key, the libraries platform and the library name.
        """

        self.__url = "https://libraries.io/api/%s/%s?api_key=%s" % (platform, name, api_key)


    def get(self):
        """
        Returns the current library info, or None if an error occurs.
        """

        library_info = None
        try:
            response = requests.get(self.__url)
            if response.status_code == 200:
                library_info = json.loads(response.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            pass
        return library_info
