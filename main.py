#!/usr/bin/python3.6

import logging
import signal
import time
from config import Config
from libchecker import LibraryChecker


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
                        format="%(asctime)s: %(name)s - %(levelname)s - %(message)s")
    logging.info("Starting main program")
    config = Config()
    checker = LibraryChecker(config.get_config())
    try:
        while True:
            checker.check()
            logging.info("Sleeping 1m")
            time.sleep(60)
    except ServiceExit:
        pass
    logging.info("Exiting main program")


if __name__ == "__main__":
    main()
