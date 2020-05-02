#!/usr/bin/env python

import pprint
from tabulate import tabulate

from genie.conf import Genie

testbed = Genie.init("testbed.yaml")
devices_info = {}

for device in testbed.devices:
    dev = testbed.devices[device]
    dev.connect(via='mgmt')
    output = dev.learn('interface')
    pprint.pprint(output.info)

    devices_info[dev.name] = []

    for intf_name,details in output.info.items():
        if ("description" in details):
           devices_info[dev.name].append((intf_name, details['enabled'],details['description'],details['bandwidth'],details['delay']))
        else:
           devices_info[dev.name].append((intf_name, details['enabled'],"",details['bandwidth'],details['delay']))

    # devices_info.append((dev.name,platform_info['os'],platform_info['version']))

print('\n' + '-'*80)

for hostname,details in devices_info.items():
    print(hostname)
    print(tabulate(details, headers=["Interface Name","Enabled","Description","Bandwidth (Kbps)","Delay"])+"\n")

print('-'*80 + '\n')

### Retrieve version info
# device_info = []
#
# for device in testbed.devices:
#     dev = testbed.devices[device]
#     dev.connect(via='mgmt')
#     output = dev.parse("show version")
#     platform_info = output['version']
#
#     device_info.append((dev.name,platform_info['os'],platform_info['version']))
#
# print('\n' + '-'*80)
#
# print(tabulate(device_info, headers=['Hostname','OS','Version']))
#
# print('-'*80 + '\n')
