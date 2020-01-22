#!/usr/bin/python3.6

from dotenv import load_dotenv
import yaml
import os


class Config():
    """
    Class that holds the configuration.
    """


    def __init__(self, yaml_file="config.yaml"):
        """
        The class requires the configuration file (default: config.yaml).
        """

        load_dotenv()
        with open(yaml_file) as yaml_content:
            self.__config = yaml.full_load(yaml_content)


    def get_configs(self):
        """
        Returns all the libchecker configurations.
        """

        return self.__config


    def get_config(self, index=0):
        """
        Returns the configuration by index.
        """

        return self.__config[index]


    def len(self):
        """
        Returns how many configurations exist.
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
        if value and isinstance(value, str) and value.startswith("env."):
            value = os.environ.get(value.split(".")[1], default)
        return value
