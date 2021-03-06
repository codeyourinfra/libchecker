#!/usr/bin/python3.6

import logging
import time
from pydoc import locate
from threading import Thread, Event
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


    def __init__(self, config):
        """
        The class requires parameters defined in the configuration file.
        """

        self.__config = config
        self.__platform = Config.get_value(self.__config, "libraries_platform")
        self.__name = Config.get_value(self.__config, "library_name")
        logging.info("Library to be checked: %s. Platform: %s.",
                     self.__name, self.__platform)

        api_key = Config.get_value(self.__config, "librariesio_api_key")
        self.__getter = LibraryInfoGetter(api_key, self.__platform, self.__name)

        mongodb_config = self.__config.get("mongodb", None)
        self.__latest = LatestLibraryInfo(**mongodb_config)


    def check(self):
        """
        Checks if a new version was released. If so,
        execute some previously defined actions.
        Always store the latest version data into MongoDB.
        """

        _id = self.get_id()
        current_info = self.__getter.get()
        latest_info = self.__latest.get(_id)

        if self.__new_version_released(current_info, latest_info):
            logging.info("New version released: %s. Previous version: %s.",
                         current_info["latest_release_number"],
                         latest_info["info"]["latest_release_number"])
            actions_config = self.__config.get("actions", None)
            for action_config in actions_config:
                self.__execute_action(action_config, current_info, latest_info)
        else:
            logging.info("No new version released yet.")

        if current_info:
            library_info = {"_id": _id, "info": current_info}
            self.__latest.set(library_info)


    def get_id(self):
        """
        Returns the libchecker id.
        """

        return "%s_%s" % (self.__platform, self.__name)


    def __new_version_released(self, current_info, latest_info):
        """
        Returns if the current version is greater than the latest.
        """

        if not current_info or not latest_info:
            return False
        current_version = current_info["latest_release_number"]
        latest_version = latest_info["info"]["latest_release_number"]
        return version.parse(current_version) > version.parse(latest_version)


    def __execute_action(self, action_config, current_info, latest_info):
        """
        Executes the pre-configured action.
        The action class must be in the actions module
        and must implement the method execute.
        """

        action_classpath = "actions.%s" % Config.get_value(action_config, "classname")
        action_class = locate(action_classpath)
        parameters = action_config["parameters"]
        action_instance = action_class(**parameters)
        logging.info("%s about to be executed...", action_classpath)
        action_instance.execute(self.__platform, self.__name, current_info, latest_info["info"])


class LibraryCheckerThread(Thread):
    """
    Thread responsible for checking the release of a library every minute.
    """


    def __init__(self, config):
        """
        The thread's name is the libchecker's id.
        """

        super().__init__()
        self.__stopped = Event()
        self.__checker = LibraryChecker(config)
        self.name = self.__checker.get_id()


    def stop(self):
        """
        Stops the thread.
        """

        self.__stopped.set()
        self.join()


    def run(self):
        """
        Checks every minute if a release was made.
        """

        while not self.__stopped.is_set():
            self.__checker.check()
            logging.info("Sleeping 1m")
            time.sleep(60)
