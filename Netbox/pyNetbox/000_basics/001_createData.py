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

### Creating objects

## Retrieving Object attributes prior to creation

ndev_site=nb.dcim.sites.get(q="hq1")
ndev_dtype=nb.dcim.device_types.get(q="7200 Series")
ndev_drole=nb.dcim.device_roles.get(q="network-core")

req_fields = (
    "Site: {site}, ID: {site_id}\n"
    "Device Type: {dtype}, ID: {dtype_id}\n"
    "Device Role: {drole}, ID: {drole_id}".format(
    site=ndev_site,
    site_id=ndev_site.id,
    dtype=ndev_dtype,
    dtype_id=ndev_dtype.id,
    drole=ndev_drole,
    drole_id=ndev_drole.id,
))

print(req_fields)

## Creating objects by retrieving the attributes prior
try:
    result = nb.dcim.devices.create([
        {
            "name": "r2",
            "device_type": ndev_dtype.id,
            "device_role": ndev_drole.id,
            "site": ndev_site.id
        }
    ])
except pynetbox.core.query.RequestError as e:
    print(e.error)

## Creating objects by specifying attributes in a dictionary
# List of dictionaries used to bulk create
# try:
#     result = nb.dcim.devices.create([
#         {
#             "name": "r2",
#             "device_type": {
#                 "slug": "7200-series"
#             },
#             "device_role": {
#                 "name": "network-core"
#             },
#             "site": {
#                 "name": "hq1"
#             }
#         }
#     ])
# except pynetbox.core.query.RequestError as e:
#     print(e.error)
