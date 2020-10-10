#!/usr/bin/env python

from genie.conf import Genie
from time import sleep

# Import custom modules
import utils.get_from_netbox as netbox
import utils.get_from_pyats as pyats
import utils.tests as test

if __name__ == "__main__":
    testbed = Genie.init("testbed.yml")

    while True:
        print(f"{'*'*32} BEGINNING CHECKS {'*'*32}\n")
        for device_name,device_details in testbed.devices.items():
            print(f"{'-'*32} {device_name} {'-'*32}\n")

            print(f"Retrieving current status from device with pyATS")
            pyats_interfaces = pyats.interfaces_current(testbed, device_name)

            print(f"Looking up intended state for device from NetBox")
            netbox_interfaces = netbox.interfaces_sot(device_name)

            print("Running interface enabled test")
            interface_enabled_test = test.verify_interface_enabled(netbox_interfaces,pyats_interfaces)

            print("Running interface description test")
            interface_description_test = test.verify_interface_description(netbox_interfaces, pyats_interfaces)

            ### Implement fixes for improper items

            if (len(interface_enabled_test['FAILED']) > 0):
                print("Updating interface enabled states")
                pyats.interface_enable_state_configure(testbed, device_name,interface_enabled_test['FAILED'])

            if (len(interface_description_test['FAILED']) > 0):
                print("Updating interface descriptions")
                pyats.interface_description_configure(testbed, device_name,interface_description_test['FAILED'])


        # Wait 10 seconds and check again
        print(f"\n{'*'*33} END OF CHECKS {'*'*34}\n")
        sleep(10)
