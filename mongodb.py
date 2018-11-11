#!/usr/bin/python3.6

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class LatestLibraryInfo():


    def __init__(self, uri, dbuser, dbpassword, dbauth, dbname):
        client = MongoClient(uri, username=dbuser, password=dbpassword, authSource=dbauth)
        self.__collection = client[dbname]["latest"]

    def get(self, _id):
        try:
            return self.__collection.find_one(_id)
        except PyMongoError:
            return None


    def set(self, library_info):
        self.__collection.replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
