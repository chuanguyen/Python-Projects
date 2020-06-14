#!/usr/bin/env python

import os
import sys
import pprint
from netaddr import *
import pynetbox
import csv
from jinja2 import Template

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Read from CSV for NetBox device data
nb_source_file = "nb_devices.csv"

nb_all_devices = list()
nb_all_devices_primaryIPs = dict()

# Stores non-existent NetBox objects defined in CSV
nb_non_existent_count = 0
nb_non_existent_objects = dict()
nb_non_existent_objects['site'] = list()
nb_non_existent_objects['device_type'] = list()
nb_non_existent_objects['device_role'] = list()
nb_non_existent_objects['rack'] = list()

fmt = "{:<15}{:<25}{:<15}"
header = ("Model","Name","Status")

try:
    with open(nb_source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
          ndev_site = nb.dcim.sites.get(slug=row['site'])
          ndev_dtype = nb.dcim.device_types.get(slug=row['device_type'])
          ndev_drole = nb.dcim.device_roles.get(slug=row['device_role'])
          ndev_rack = nb.dcim.racks.get(q=row['rack'])

          # Verifies whether DCIM object exists
          if (not ndev_site):
              nb_non_existent_objects['site'].append(row['site'])
              nb_non_existent_count += 1
          if (not ndev_dtype):
              nb_non_existent_objects['device_type'].append(row['device_type'])
              nb_non_existent_count += 1
          if (not ndev_drole):
              nb_non_existent_objects['device_role'].append(row['device_type'])
              nb_non_existent_count += 1
          if (not ndev_rack):
              nb_non_existent_objects['rack'].append(row['rack'])
              nb_non_existent_count += 1

          # Generates dict of values for PyNetbox to create object
          nb_all_devices.append(
            dict(
                name=row['name'],
                site=ndev_site,
                device_type=ndev_dtype.id,
                device_role=ndev_drole.id,
                rack=ndev_rack.id,
                face=row['face'],
                position=row['position'],
                serial=row['serial'],
                asset_tag=row['asset_tag'],
                status=row['status'],
            )
          )

          nb_all_devices_primaryIPs[row['name']] = row['primary_ipv4']

except FileNotFoundError as e:
    print(e)
except pynetbox.core.query.RequestError as e:
    print(e.error)

### Generates table of non-existent NetBox objects defined in CSV
if (nb_non_existent_count > 0):
    print(12*"*"," Verify the following NetBox Objects ",12*"*")
    print(fmt.format(*header))

    # Print summary of non-existent objects in CSV
    for model,nb_objects in nb_non_existent_objects.items():
        for nb_object in nb_objects:
            print(
                fmt.format(
                    model,
                    nb_object,
                    "Non-Existent"
                )
            )

pprint.pprint(nb_all_devices)
pprint.pprint(nb_all_devices_primaryIPs)



# ### Creating Spine and Leaf devices
#
# SPINE_NUM = 2
# LEAF_NUM = 4
#
# # List to store dictionary attributes
# ndev_list = list()
#
# ndev_site = nb.dcim.sites.get(slug="hq1")
# ndev_dtype = nb.dcim.device_types.get(slug="7200-series")
# ndev_drole_spine = nb.dcim.device_roles.get(slug="network-core")
# ndev_drole_leaf = nb.dcim.device_roles.get(slug="network-access")
#
# # Generate spine attributes
#
# for i in range(1,SPINE_NUM+1):
#     ndev_list.append(
#         dict(
#             name="sw-spine-0{swid}".format(swid=i),
#             device_type=ndev_dtype.id,
#             device_role=ndev_drole_spine.id,
#             site=ndev_site.id,
#         )
#     )
#
# # Generate leaf attributes
#
# for i in range(1,LEAF_NUM+1):
#     ndev_list.append(
#         dict(
#             name="sw-leaf-0{swid}".format(swid=i),
#             device_type=ndev_dtype.id,
#             device_role=ndev_drole_leaf.id,
#             site=ndev_site.id,
#         )
#     )
#
# try:
#
#     # Retrieve device object by name and delete
#     for dev in ndev_list:
#         nb_dev = nb.dcim.devices.get(name=dev['name'])
#         nb_dev.delete()
#
#     results = nb.dcim.devices.create(ndev_list)
#
#     # Formatting and header for output
#     fmt = "{:<25}{:<25}{:<25}{:<15}"
#     header = ("Device", "Dev Role", "Dev Type", "Site")
#     print(fmt.format(*header))
#
#     # Print summary info for each created device
#     for r in results:
#         print(
#             fmt.format(
#                 r.name,
#                 r.device_role.name,
#                 r.device_type.model,
#                 r.site.name,
#             )
#         )
#
# except pynetbox.core.query.RequestError as e:
#     print(e.error)
