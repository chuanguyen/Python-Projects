#!/usr/bin/env python

from genie.conf import Genie
from time import sleep

# Import custom modules
import utils.get_from_netbox as netbox
import utils.get_from_pyats as pyats

if __name__ == "__main__":
    testbed = Genie.init("testbed.yml")

    while True:
        for device in testbed.devices:
            netbox_interfaces = netbox.interfaces_sot(device)
            print(netbox_interfaces)


        # Wait 10 seconds and check again
        sleep(10)
