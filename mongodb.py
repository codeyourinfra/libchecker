#!/usr/bin/python3.6

from pymongo import MongoClient


class LibraryInfoSetter():


    def __init__(self, mongodb_uri, dbuser, dbpassword, dbauth, dbname):
        self.__db = MongoClient(mongodb_uri, username=dbuser, password=dbpassword, authSource=dbauth)[dbname]


    def set(self, library_info):
        self.__db["latest"].replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
