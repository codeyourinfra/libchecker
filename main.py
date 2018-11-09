#!/usr/bin/python3.6

import logging
import signal
import time
from libchecker import LibraryChecker


logger = logging.getLogger("libchecker")
handler = logging.StreamHandler("ext://sys.stdout")
formatter = logging.Formatter("%(asctime)s: %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum):
    logger.info('Caught signal %d' % signum)
    raise ServiceExit


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    logger.info("Starting main program")
    checker = LibraryChecker()
    try:
        while True:
            checker.check()
            time.sleep(60)
    except ServiceExit:
        pass
    logger.info("Exiting main program")


if __name__ == "__main__":
    main()
