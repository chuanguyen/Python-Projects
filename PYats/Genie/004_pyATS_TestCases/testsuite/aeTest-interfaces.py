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
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect(via='mgmt')
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################


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
    def check_interface_status(self):
        """ Sample test section. Only print """

        failed_dict = {}
        mega_tabular = {}

        for device, interfaces in self.all_interfaces.items():
            mega_tabular[device] = []

            for intf_name, details in interfaces.items():
                tr = []

                if ("description" in details):
                   tr.append(intf_name)
                   tr.append(details['enabled'])
                   tr.append(details['description'])

                   if ( details['description'] == "Automation Shutdown" and details['enabled'] ):
                       failed_dict[device] = {}
                       failed_dict[device] = details
                       tr.append("Failed")
                   else:
                       tr.append("Passed")

                else:
                   tr.append(intf_name)
                   tr.append(details['enabled'])
                   tr.append("")

                   if ( details['enabled'] ):
                       failed_dict[device] = {}
                       failed_dict[device] = details
                       tr.append("Failed")
                   else:
                       tr.append("Passed")


                mega_tabular[device].append(tr)


        for hostname,details in mega_tabular.items():
            log.info(hostname)

            log.info(tabulate(details,
                              headers=['Interface', 'Status',
                                       'Description', 'Pass/Fail'],
                              tablefmt='orgtbl'))

        if failed_dict:
            log.error(json.dumps(failed_dict, indent=3))
            self.failed("There are interfaces in an improper state")

        else:
            self.passed("All interfaces are in the proper state")

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