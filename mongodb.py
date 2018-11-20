#!/usr/bin/python3.6

import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config


class LatestLibraryInfo():
    """
    Class responsible for storing the latest library info into MongoDB.
    """


    def __init__(self, **config):
        """
        The class requires MongoDB connection parameters.
        """

        uri = Config.get_value(config, "uri")
        dbuser = Config.get_value(config, "username")
        dbpassword = Config.get_value(config, "password")
        dbauth = Config.get_value(config, "dbauth", "admin")
        dbname = Config.get_value(config, "dbname", "libraries")
        client = MongoClient(uri, username=dbuser, password=dbpassword, authSource=dbauth)
        self.__collection = client[dbname]["latest"]


    def get(self, _id):
        """
        Returns the latest library info, or None if an error occurs.
        """

        try:
            library_info = self.__collection.find_one(_id)
            logging.info("Success on getting the latest library info.")
        except PyMongoError:
            logging.exception("Error on getting the latest library info. Stack trace:")
            library_info = None
        return library_info


    def set(self, library_info):
        """
        Stores the latest library info.
        """

        try:
            self.__collection.replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
            logging.info("Success on storing the latest library info.")
        except PyMongoError:
            logging.exception("Error on storing the latest library info. Stack trace:")
