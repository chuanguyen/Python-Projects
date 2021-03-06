#!/usr/bin/env python

import pprint
from tabulate import tabulate

from genie.conf import Genie

testbed = Genie.init("testbed.yaml")

dev = testbed.devices['R1']
dev.connect(via='mgmt')
output = dev.learn('hsrp')
pprint.pprint(output.info)

mega_tabular = {}
failed_dict = {}

for intf_name,hsrp_details in output.info.items():
    mega_tabular[dev.name] = []
    tr = []

    for hsrp_group,hsrp_group_config in hsrp_details['address_family']['ipv4']['version'][2]['groups'].items():
        print(hsrp_group)
        print(hsrp_group_config)
        print(hsrp_details['interface'])




# devices_info = {}
#
# for device in testbed.devices:
#     dev = testbed.devices[device]
#     dev.connect(via='mgmt')
#     output = dev.learn('interface')
#
#     # Mega table containing interface info for each device
#     devices_info[dev.name] = []
#
#     for intf_name,details in output.info.items():
#         # Represents a row containing interface info
#         tr = []
#
#         if ("description" in details):
#            tr.append(intf_name)
#            tr.append(details['enabled'])
#            tr.append(details['description'])
#            tr.append(details['bandwidth'])
#            tr.append(details['delay'])
#            devices_info[dev.name].append(tr)
#         else:
#            tr.append(intf_name)
#            tr.append(details['enabled'])
#            tr.append("")
#            tr.append(details['bandwidth'])
#            tr.append(details['delay'])
#            devices_info[dev.name].append(tr)
#
# print('\n' + '-'*80)
#
# for hostname,details in devices_info.items():
#     print(hostname)
#     print(tabulate(details, headers=["Interface Name","Enabled","Description","Bandwidth (Kbps)","Delay"])+"\n")
#
# print('-'*80 + '\n')

### Retrieve version info
# device_info = []
#
# for device in testbed.devices:
#     dev = testbed.devices[device]
#     dev.connect(via='mgmt')
#     output = dev.parse("show version")
#     platform_info = output['version']
#
#     tr = []
#     tr.append(dev.name)
#     tr.append(platform_info['os'])
#     tr.append(platform_info['version'])
#     device_info.append(tr)
#
# print('\n' + '-'*80)
#
# print(tabulate(device_info, headers=['Hostname','OS','Version']))
#
# print('-'*80 + '\n')
