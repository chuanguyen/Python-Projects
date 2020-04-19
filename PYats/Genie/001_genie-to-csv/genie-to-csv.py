#!/usr/bin/env python

from genie.conf import Genie
from genie.testbed import load
import csv


testbed = Genie.init("testbed.yaml")

interface_details = {}

for device in testbed.devices:
    dev = testbed.devices[device]
    dev.connect()
    interfaces = dev.parse("show interfaces")
    interface_details[device] = interfaces

interface_file = "interfaces.csv"
report_fields = ["Hostname","Interface","MAC Address"]

with open (interface_file, "w") as f:
    writer = csv.DictWriter(f, report_fields)
    writer.writeheader()

    for device,interfaces in interface_details.items():
        for if_name,details in interfaces.items():
            if (("mac_address" in details.keys())):
                writer.writerow(
                                {"Hostname": device,
                                 "Interface": if_name,
                                 "MAC Address": details["mac_address"]
                                })
