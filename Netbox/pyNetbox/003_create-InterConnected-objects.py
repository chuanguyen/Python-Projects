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

### Creating Spine and Leaf devices

SPINE_NUM = 2
LEAF_NUM = 4
ip_addr_count = 1

# List to store dictionary attributes
ndev_list = list()
ndev_primaryIPs = dict()

ndev_site = nb.dcim.sites.get(slug="hq1")
ndev_dtype = nb.dcim.device_types.get(slug="7200-series")
ndev_drole_spine = nb.dcim.device_roles.get(slug="network-core")
ndev_drole_leaf = nb.dcim.device_roles.get(slug="network-access")

# Generate spine attributes

for i in range(1,SPINE_NUM+1):
    ndev_list.append(
        dict(
            name="sw-spine-0{swid}".format(swid=i),
            device_type=ndev_dtype.id,
            device_role=ndev_drole_spine.id,
            site=ndev_site.id,
        )
    )

# Generate leaf attributes

for i in range(1,LEAF_NUM+1):
    ndev_list.append(
        dict(
            name="sw-leaf-0{swid}".format(swid=i),
            device_type=ndev_dtype.id,
            device_role=ndev_drole_leaf.id,
            site=ndev_site.id,
        )
    )

# Generate primary IPs for spines and leafs
for new_dev in ndev_list:
    ndev_primaryIPs[new_dev['name']] = "10.10.10.10{host_ip}/24".format(host_ip=ip_addr_count)
    ip_addr_count += 1

try:

    # Retrieve device object by name and delete
    for dev in ndev_list:
        nb_dev = nb.dcim.devices.get(name=dev['name'])
        nb_dev.delete()

    # Add devices to NetBox and store resulting object in "new_devs"
    new_devs = nb.dcim.devices.create(ndev_list)

    # Formatting and header for output
    fmt = "{:<20}{:<20}{:<15}{:<10}{:<25}{:<20}"
    header = ("Device", "Dev Role", "Dev Type", "Site", "Management Interface", "IP")
    print(fmt.format(*header))

    # Print summary info for each created device
    for new_dev in new_devs:
        # Retrieve specific interface associated w/ created device
        nb_interfaces = nb.dcim.interfaces.filter(device=new_dev.name,name="FastEthernet0/0")

        # Create dict to store attributes for device's primary IP
        primary_ip_addr_dict = dict(
            address=ndev_primaryIPs[new_dev.name],
            status=1,
            description="Management IP for {}".format(new_dev.name),
            interface=nb_interfaces[0].id,
        )

        # Create primary IP and assign to device's first interface
        new_primary_ip = nb.ipam.ip_addresses.create(primary_ip_addr_dict)

        print(
            fmt.format(
                new_dev.name,
                new_dev.device_role.name,
                new_dev.device_type.model,
                new_dev.site.name,
                nb_interfaces[0].name,
                new_primary_ip.address
            )
        )

except pynetbox.core.query.RequestError as e:
    print(e.error)
