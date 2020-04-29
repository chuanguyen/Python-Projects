#!/usr/bin/env python

from genie.conf import Genie
import pprint


testbed = Genie.init("testbed.yaml")

### Testing



# for device in testbed.devices:
#     dev = testbed.devices[device]
#     dev.connect()
#     interfaces = dev.parse("show interfaces")
#     interface_details[device] = interfaces
#
# interface_file = "interfaces.csv"
#
# with open (interface_file, "w") as f:


### Retrieving learned features via different connection

# baseline = {}
#
# for hostname,dev in testbed.devices.items():
#     dev.connect(via='mgmt')
#     baseline[hostname] = {}
#     baseline[hostname]["interface"] = dev.learn("interface")
#     pprint.pprint(baseline[hostname]["interface"].info)

### Retrieving learned features

# baseline = {}
#
# for hostname,dev in testbed.devices.items():
#     dev.connect()
#     baseline[hostname] = {}
#     baseline[hostname]["interface"] = dev.learn("interface")
#     pprint.pprint(baseline[hostname]["interface"].info)


### Retrieving learned features w/ many connection entries

# for hostname,dev in testbed.devices.items():
#     dev.connect(alias='vty_1', via='mgmt')
#     baseline[hostname] = {}
#     baseline[hostname]["interface"] = dev.learn("interface")
#     pprint.pprint(baseline[hostname]["interface"].info)
