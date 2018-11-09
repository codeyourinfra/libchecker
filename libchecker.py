#!/usr/bin/python3.6

import os
import json
from librariesio import LibraryInfoGetter
from mongodb import LibraryInfoSetter


class LibraryChecker():


    def __init__(self):
        api_key = os.environ.get("LIBRARIESIO_API_KEY")
        self.__platform = os.environ.get("LIBRARIES_PLATFORM")
        self.__name = os.environ.get("LIBRARY_NAME")
        self.__getter = LibraryInfoGetter(api_key, self.__platform, self.__name)

        uri = os.environ.get("MONGODB_URI")
        dbuser = os.environ.get("MONGODB_USERNAME")
        dbpassword = os.environ.get("MONGODB_PASSWORD")
        dbauth = os.environ.get("MONGODB_DBAUTH")
        dbname = os.environ.get("MONGODB_DBNAME", dbauth)
        self.__setter = LibraryInfoSetter(uri, dbuser, dbpassword, dbauth, dbname)


    def check(self):
        _id = "%s_%s" % (self.__platform, self.__name)
        info = json.loads(self.__getter.get())
        library_info = {"_id": _id, "info": info}
        self.__setter.set(library_info)
