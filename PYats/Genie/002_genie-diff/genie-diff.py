#!/usr/bin/env python

from genie.conf import Genie
import pprint


testbed = Genie.init("testbed.yaml")

### Retrieving learned features

baseline = {}

for hostname,dev in testbed.devices.items():
    dev.connect()
    baseline[hostname] = {}
    baseline[hostname]["interface"] = dev.learn("interface")
    pprint.pprint(baseline[hostname]["interface"].info)


# for device in testbed.devices:
#     dev = testbed.devices[device]
#     dev.connect()
#     interfaces = dev.parse("show interfaces")
#     interface_details[device] = interfaces
#
# interface_file = "interfaces.csv"
#
# with open (interface_file, "w") as f:



### Retrieving learned features

# baseline = {}
#
# for hostname,dev in testbed.devices.items():
#     dev.connect()
#     baseline[hostname] = {}
#     baseline[hostname]["interface"] = dev.learn("interface")
#     pprint.pprint(baseline[hostname]["interface"].info)
