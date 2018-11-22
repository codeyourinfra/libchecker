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


    def get_config(self, index=0):
        """
        Returns the configuration by index.
        """

        return self.__config[index]


    def len(self):
        """
        Returns how many configurations are.
        """

        return len(self.__config)


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
