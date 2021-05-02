#!/bin/env python

# To get a logger for the script
import logging
import json
# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from ats import aetest
from ats.log.utils import banner

# Genie Imports
from genie.conf import Genie
from genie.abstract import Lookup

# import the genie libs
from genie.libs import ops # noqa

# Get your logger for your script
log = logging.getLogger(__name__)


###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        devices_to_ignore = [
            "terminal_server"
        ]

        for device in genie_testbed.devices.values():
            if device.name not in devices_to_ignore:
                log.info(banner(
                    "Connect to device '{d}'".format(d=device.name)))
                try:
                    device.connect()
                except Exception as e:
                    self.failed("Failed to establish connection to '{}'".format(device.name))

                device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################
""" This is user Testcases section """

class Interface_Status_Verify(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def learn_interfaces(self):
        """ Sample test section. Only print """

        self.all_interfaces = {}
        for dev in self.parent.parameters['dev']:
            log.info(banner("Gathering interface Information from {}".format(
                dev.name)))
            interfaces = dev.learn("interface")
            self.all_interfaces[dev.name] = interfaces.info

    @ aetest.test
    def check_interface_description(self):
        """ Sample test section. Only print """

        description_test_passed = True
        failed_devices = set()
        devices_interfaces_dict = {}

        for device, interfaces in self.all_interfaces.items():
            devices_interfaces_dict[device] = []

            for intf_name, intf_details in interfaces.items():
                tr = []

                tr.append(intf_name)
                tr.append(intf_details['enabled'])

                if ("description" in intf_details):
                   tr.append(intf_details['description'])
                   tr.append("Passed")
                else:
                    tr.append("NO DESCRIPTION SET")
                    tr.append("Failed")
                    description_test_passed = False
                    failed_devices.add(device)

                devices_interfaces_dict[device].append(tr)


        for hostname,details in devices_interfaces_dict.items():
            log.info(hostname)
            log.info(tabulate(details,
                              headers=['Interface', 'Enabled',
                                       'Description', 'Pass/Fail'],
                              tablefmt='orgtbl'))

        if description_test_passed:
            self.passed("All interfaces have a description set")
        else:
            log.error(json.dumps(list(failed_devices), indent=3))
            self.failed("There are devices with interfaces missing descriptions")

# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
