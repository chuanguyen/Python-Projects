#!/usr/bin/env python

import os
import sys
import pprint
from netaddr import *
import pynetbox

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Retrieving an available IP from a prefix, and deleting or creating it
# single_prefix = nb.ipam.prefixes.get(q="192.168.100.0", mask_length=24)
# # Output is capped to 50 items by default
# available_ips = single_prefix.available_ips.list()
# pprint.pprint(available_ips)
#
# single_ip = nb.ipam.ip_addresses.get(q="192.168.100.1")
# # single_ip.delete()
# # single_ip.create()

### Retrieve device type based on retrieved devices
# devices = nb.dcim.devices.all()
#
# for device in devices:
#     device_type = nb.dcim.device_types.get(device.device_type.id)
#     print(
#         "Manufacturer: {manuf} - Model: {model}".format (
#             manuf=device_type.manufacturer, model=device_type.model
#         )
#     )

### Getting a particular object
# single_prefix = nb.ipam.prefixes.get(q="10.1.1.0", mask_length=24)
#
# print(single_prefix)

### Filtering based on specific attributes
# pfx_search = nb.ipam.prefixes.filter(within="10.0.0.0/8", status="active")
#
# print(pfx_search)
# print()
# for pfx in pfx_search:
#     print(pfx.prefix, pfx.status.value)

### Retrieve prefixes and output attributes
# Returns a list of prefix objects, not strings
# all_prefixes = nb.ipam.prefixes.all()
#
# fmt = "{:<20}{:<20}{:<20}{:<20}" # Indicates all items are left-aligned w/ a width of 20
# header = ("Prefix", "Status", "Site", "Role")
#
# print(fmt.format(*header))
# for prefix in all_prefixes:
#     print (
#         fmt.format(
#             prefix.prefix,
#             prefix.status.label,
#             prefix.site.name,
#             prefix.role.name,
#         )
#     )

### Retrieving IP and network address info
# In prior versions of Netbox, the prefix
# attribute was a netaddr object, but newer versions
# have the attribute as as str
# my_pfx = all_prefixes[3]
# my_prefix_netaddr = IPNetwork(my_pfx.prefix)
# print(my_prefix_netaddr.netmask)
