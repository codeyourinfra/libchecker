#!/usr/bin/python3.6

import json
import logging
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
                logging.info("Success on getting the current library info.")
            else:
                logging.warning("Failure on getting the current library info. "
                                "Status code: %s. Webhook response: %s",
                                response.status_code, response.text)
        except requests.exceptions.ConnectionError:
            logging.exception("Error on getting the current library info. Stack trace:")
        return library_info
