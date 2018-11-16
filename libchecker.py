#!/usr/bin/python3.6

import logging
from pydoc import locate
from packaging import version
from config import Config
from librariesio import LibraryInfoGetter
from mongodb import LatestLibraryInfo


class LibraryChecker():
    """
    Class responsible for checking if a new
    version of some library was released in
    order to take one or more actions.
    """


    def __init__(self):
        """
        The class requires parameters defined in config.json
        """

        self.__config = Config()
        self.__platform = self.__config.get_libraries_platform()
        self.__name = self.__config.get_library_name()

        api_key = self.__config.get_librariesio_api_key()
        self.__getter = LibraryInfoGetter(api_key, self.__platform, self.__name)

        mongodb_config = self.__config.get_mongodb_config()
        self.__latest = LatestLibraryInfo(**mongodb_config)


    def check(self):
        """
        Checks if a new version was released. If so,
        execute some previously defined actions.
        Always store the latest version data into MongoDB.
        """

        _id = "%s_%s" % (self.__platform, self.__name)
        current_info = self.__getter.get()
        latest_info = self.__latest.get(_id)

        if self.__new_version_released(current_info, latest_info):
            actions_config = self.__config.get_actions_config()
            for action_config in actions_config:
                self.__execute_action(action_config, current_info, latest_info)
        else:
            logging.info("No version released yet.")

        if current_info:
            library_info = {"_id": _id, "info": current_info}
            self.__latest.set(library_info)


    def __new_version_released(self, current_info, latest_info):
        if not current_info or not latest_info:
            return False
        current_version = current_info["latest_release_number"]
        latest_version = latest_info["info"]["latest_release_number"]
        return version.parse(current_version) > version.parse(latest_version)


    def __execute_action(self, action_config, current_info, latest_info):
        action_classpath = "actions.%s" % Config.get_value(action_config, "classname")
        action_class = locate(action_classpath)
        parameters = action_config["parameters"]
        action_instance = action_class(**parameters)
        logging.info("%s about to be executed...", action_classpath)
        action_instance.execute(self.__platform, self.__name, current_info, latest_info["info"])
