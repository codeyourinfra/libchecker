#!/usr/bin/python3.6

from pymongo import MongoClient


class LibraryInfoSetter():


    def __init__(self, uri, dbuser, dbpassword, dbauth, dbname):
        client = MongoClient(uri, username=dbuser, password=dbpassword, authSource=dbauth)
        self.__db = client[dbname]


    def set(self, library_info):
        self.__db["latest"].replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
