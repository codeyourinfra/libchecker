#!/usr/bin/python3.6

import json
import os


class Config():
    """
    Class that holds the configuration.
    """


    def __init__(self, json_file="config.json"):
        """
        The class requires the file config.json.
        """

        with open(json_file) as json_content:
            self.__config = json.load(json_content)


    @staticmethod
    def get_value(node, key, default=None):
        """
        Returns the parameter value, or the default, based on the key.
        If the value starts with "env.", returns the value of the
        environment variable defined right after.
        """

        value = node.get(key, default)
        if value and value.startswith("env."):
            value = os.environ.get(value.split(".")[1], default)
        return value


    def get_librariesio_api_key(self):
        """
        Returns the Libraries.io API key.
        """

        return Config.get_value(self.__config, "librariesio_api_key")


    def get_libraries_platform(self):
        """
        Returns the libraries platform.
        """

        return Config.get_value(self.__config, "libraries_platform")


    def get_library_name(self):
        """
        Returns the library name.
        """

        return Config.get_value(self.__config, "library_name")


    def get_mongodb_config(self):
        """
        Returns the MongoDB configuration.
        """

        return self.__config["mongodb"]


    def get_actions_config(self):
        """
        Returns the actions to be executed.
        """

        return self.__config["actions"]
