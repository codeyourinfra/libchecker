#!/usr/bin/python3.6

import logging
import signal
import time
from config import Config
from libchecker import LibraryCheckerThread


class ReleaseMonitor():
    """
    Class responsible for controlling the libchecker threads lifecycle.
    """


    def __init__(self):
        self.__config = Config()
        self.__threads = []
        for config in self.__config.get_configs():
            self.__threads.append(LibraryCheckerThread(config))


    def start(self):
        """
        Starts all libchecker threads.
        """

        for thread in self.__threads:
            thread.start()


    def stop(self):
        """
        Stops all libchecker threads.
        """

        for thread in self.__threads:
            thread.stop()


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """

    pass


def service_shutdown(signum, frame):
    """
    Called when some signal is caught.
    """

    logging.info("Caught signal %d", signum)
    raise ServiceExit


def main():
    """
    Main program.
    """

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s: %(threadName)s - %(levelname)s - %(message)s")
    logging.info("Starting main program")
    monitor = ReleaseMonitor()
    try:
        monitor.start()
        while True:
            time.sleep(0.5)
    except ServiceExit:
        monitor.stop()
    logging.info("Exiting main program")


if __name__ == "__main__":
    main()
