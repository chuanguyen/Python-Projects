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

# List to store dictionary attributes
ndev_list = list()

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

try:

    # Retrieve device object by name and delete
    for dev in ndev_list:
        nb_dev = nb.dcim.devices.get(name=dev['name'])
        nb_dev.delete()

    results = nb.dcim.devices.create(ndev_list)

    # Formatting and header for output
    fmt = "{:<25}{:<25}{:<25}{:<15}"
    header = ("Device", "Dev Role", "Dev Type", "Site")
    print(fmt.format(*header))

    # Print summary info for each created device
    for r in results:
        print(
            fmt.format(
                r.name,
                r.device_role.name,
                r.device_type.model,
                r.site.name,
            )
        )

except pynetbox.core.query.RequestError as e:
    print(e.error)
