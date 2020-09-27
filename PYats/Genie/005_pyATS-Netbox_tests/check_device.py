#!/bin/env python

from genie.conf import Genie
from time import sleep

if __name__ == "__main__":
    testbed = Genie.init("testbed.yml")

    while True:
        for dev in testbed.devices:
            print(dev)


        # Wait 10 seconds and check again
        sleep(10)
