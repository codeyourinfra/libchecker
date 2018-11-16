#!/usr/bin/python3.6

import logging
import signal
import time
from libchecker import LibraryChecker


logger = logging.getLogger("libchecker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    logger.info("Caught signal %d", signum)
    raise ServiceExit


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    logger.info("Starting main program")
    checker = LibraryChecker()
    try:
        while True:
            checker.check()
            logger.info("Sleeping 1m")
            time.sleep(60)
    except ServiceExit:
        pass
    logger.info("Exiting main program")


if __name__ == "__main__":
    main()
