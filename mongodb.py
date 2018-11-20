#!/usr/bin/python3.6

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
            return self.__collection.find_one(_id)
        except PyMongoError:
            return None


    def set(self, library_info):
        """
        Stores the latest library info.
        """

        self.__collection.replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
