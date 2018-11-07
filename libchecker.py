#!/usr/bin/python3.6

import os
import json
import requests
from requests.exceptions import ConnectionError
from pymongo import MongoClient


class LibraryInfoGetter():

    def __init__(self, api_key, platform, name):
        self.__url = "https://libraries.io/api/%s/%s?api_key=%s" % (platform, name, api_key)

    def get(self):
        try:
            response = requests.get(self.__url)
            library_info = response.content.decode("utf-8") if response.status_code == 200 else ""
        except ConnectionError:
            library_info = ""
        return library_info


class LibraryInfoSetter():

    def __init__(self, mongodb_uri, dbuser, dbpassword, dbname):
        self.__db = MongoClient(mongodb_uri, username=dbuser, password=dbpassword)[dbname]

    def set(self, library_info):
        self.__db["libraries"].replace_one({"_id": library_info["_id"]}, library_info, upsert=True)


def main():
    api_key = os.environ.get("LIBRARIESIO_API_KEY")
    platform = os.environ.get("LIBRARIES_PLATFORM")
    name = os.environ.get("LIBRARY_NAME")
    getter = LibraryInfoGetter(api_key, platform, name)

    mongodb_uri = os.environ.get("MONGODB_URI")
    dbuser = os.environ.get("MONGODB_USERNAME")
    dbpassword = os.environ.get("MONGODB_PASSWORD")
    dbname = os.environ.get("MONGODB_NAME")
    setter = LibraryInfoSetter(mongodb_uri, dbuser, dbpassword, dbname)

    id = "%s_%s" % (platform, name)
    info = json.loads(getter.get())
    library_info = {"_id": id, "info": info}
    setter.set(library_info)


if __name__ == "__main__":
    main()
