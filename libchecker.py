#!/usr/bin/python3.6

import os
import json
from librariesio import LibraryInfoGetter
from mongodb import LibraryInfoSetter


class LibraryChecker():


    def __init__(self):
        self.__getter = self.__getGetter()
        self.__setter = self.__getSetter()


    def __getGetter(self):
        self.__api_key = os.environ.get("LIBRARIESIO_API_KEY")
        self.__platform = os.environ.get("LIBRARIES_PLATFORM")
        self.__name = os.environ.get("LIBRARY_NAME")
        return LibraryInfoGetter(self.__api_key, self.__platform, self.__name)


    def __getSetter(self):
        self.__mongodb_uri = os.environ.get("MONGODB_URI")
        self.__dbuser = os.environ.get("MONGODB_USERNAME")
        self.__dbpassword = os.environ.get("MONGODB_PASSWORD")
        self.__dbname = os.environ.get("MONGODB_NAME")
        return LibraryInfoSetter(self.__mongodb_uri, self.__dbuser, self.__dbpassword, self.__dbname)


    def check(self):
        id = "%s_%s" % (self.__platform, self.__name)
        info = json.loads(self.__getter.get())
        library_info = {"_id": id, "info": info}
        self.__setter.set(library_info)
