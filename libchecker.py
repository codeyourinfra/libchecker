#!/usr/bin/python3.6

import os
import json
from librariesio import LibraryInfoGetter
from mongodb import LibraryInfoSetter


class LibraryChecker():
    """
    Class responsible for checking if a new
    version of some library was released in
    order to take an specific action.
    """


    def __init__(self):
        """
        The class requires the following environment variables:
        LIBRARIESIO_API_KEY - the libraries.io API key
        LIBRARIES_PLATFORM - the platform from where library data is extracted (ex: pypi)
        LIBRARY_NAME - the name of the library
        MONGODB_URI - the URI of a MongoDB instance where the latest library data is kept
        MONGODB_USERNAME - the MongoDB username
        MONGODB_PASSWORD - the password for connecting to MongoDB
        MONGODB_DBAUTH - the database where the user can connect to (if root, admin)
        MONGODB_DBNAME - the database where the latest library data is stored (default to libraries)
        """

        api_key = os.environ.get("LIBRARIESIO_API_KEY")
        self.__platform = os.environ.get("LIBRARIES_PLATFORM")
        self.__name = os.environ.get("LIBRARY_NAME")
        self.__getter = LibraryInfoGetter(api_key, self.__platform, self.__name)

        uri = os.environ.get("MONGODB_URI")
        dbuser = os.environ.get("MONGODB_USERNAME")
        dbpassword = os.environ.get("MONGODB_PASSWORD")
        dbauth = os.environ.get("MONGODB_DBAUTH", "admin")
        dbname = os.environ.get("MONGODB_DBNAME", "libraries")
        self.__setter = LibraryInfoSetter(uri, dbuser, dbpassword, dbauth, dbname)


    def check(self):
        """
        Checks if a new version was released. If so,
        store the latest version data into MongoDB
        and execute some previsouly defined action.
        """

        _id = "%s_%s" % (self.__platform, self.__name)
        info = json.loads(self.__getter.get())
        library_info = {"_id": _id, "info": info}
        self.__setter.set(library_info)
