#!/usr/bin/python3.6

import json
import os


class Config():
    """
    Class that holds the configuration
    """


    def __init__(self):
        with open("config.json") as json_file:
            self.__config = json.load(json_file)


    @staticmethod
    def get_value(node, key, default=None):
        value = node.get(key, default)
        if value and value.startswith("env."):
            value = os.environ.get(value.split(".")[1], default)
        return value


    def get_librariesio_api_key(self):
        return Config.get_value(self.__config, "librariesio_api_key")


    def get_libraries_platform(self):
        return Config.get_value(self.__config, "libraries_platform")


    def get_library_name(self):
        return Config.get_value(self.__config, "library_name")


    def get_mongodb_config(self):
        return self.__config["mongodb"]


    def get_actions_config(self):
        return self.__config["actions"]
