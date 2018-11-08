#!/usr/bin/python3.6

from pymongo import MongoClient


class LibraryInfoSetter():


    def __init__(self, mongodb_uri, dbuser, dbpassword, dbname):
        self.__db = MongoClient(mongodb_uri, username=dbuser, password=dbpassword)[dbname]


    def set(self, library_info):
        self.__db["libraries"].replace_one({"_id": library_info["_id"]}, library_info, upsert=True)
