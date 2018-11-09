#!/usr/bin/python3.6

import signal
import time
from libchecker import LibraryChecker


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print("Starting main program")
    checker = LibraryChecker()
    try:
        while True:
            checker.check()
            time.sleep(60)
    except ServiceExit:
        pass
    print("Exiting main program")


if __name__ == "__main__":
    main()
