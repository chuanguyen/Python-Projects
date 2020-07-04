#!/usr/bin/env python

import os
import sys
import pprint
from netaddr import *
import pynetbox
import csv
import yaml

def retrieve_nb_id(app, model, searchTerm):
    # Searches for a NetBox object of a given model based on a search term and returns the ID
    nb_obj_id = None
    nb_obj = None

    if (app == "dcim"):
        if (model == "regions"):
            nb_obj = nb.dcim.regions.get(name=searchTerm)
        elif (model == "sites"):
            nb_obj = nb.dcim.sites.get(name=searchTerm)
        elif (model == "rack_roles"):
            nb_obj = nb.dcim.rack_roles.get(name=searchTerm)
        elif (model == "rack_groups"):
            nb_obj = nb.dcim.rack_groups.get(name=searchTerm)
        elif (model == "racks"):
            nb_obj = nb.dcim.racks.get(name=searchTerm)

    if (nb_obj):
        nb_obj_id = nb_obj.id

    return nb_obj_id

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Read from CSV for NetBox device data
nb_source_file = "base_nb_objects.yml"

try:
    with open(nb_source_file) as f:
        nb_base_data = yaml.load(f, Loader=yaml.FullLoader)
except NameError as e:
    print(e)

# Stores non-existent NetBox objects defined in CSV
created_nb_count = 0
created_nb_objects = dict()

# DCIM App & models
created_nb_objects['dcim'] = dict()
created_nb_objects['dcim'] = list()


# IPAM App & models
created_nb_objects['ipam'] = dict()
created_nb_objects['ipam']['rirs'] = list()
created_nb_objects['ipam']['aggregates'] = list()
created_nb_objects['ipam']['prefixes'] = list()
created_nb_objects['ipam']['prefix_vlan_roles'] = list()
created_nb_objects['ipam']['vlans'] = list()
created_nb_objects['ipam']['vlan_groups'] = list()

fmt = "{:<15}{:<25}{:<15}"
header = ("Model","Name","Status")

# Cycle through DCIM objects
for model,nb_obj_dicts in nb_base_data['dcim'].items():
    for nb_obj_dict in nb_obj_dicts:
        if (nb_obj_dict):
            nb_obj = None

            try:
                if (model == "regions"):
                    # Attempts to retrieves object, and creates if object doesn't exist
                    nb_obj = nb.dcim.regions.get(name=nb_obj_dict['name'])
                    if (not nb_obj):
                        nb.dcim.regions.create(nb_obj_dict)
                elif (model == "sites"):
                    nb_obj = nb.dcim.sites.get(name=nb_obj_dict['name'])
                    if (not nb_obj):
                        # Replacing fields that require NetBox IDs as values
                        nb_obj_dict['region'] = retrieve_nb_id("dcim","regions",nb_obj_dict['region'])

                        nb.dcim.sites.create(nb_obj_dict)
                elif (model == "rack_roles"):
                    nb_obj = nb.dcim.rack_roles.get(name=nb_obj_dict['name'])
                    if (not nb_obj):
                        nb.dcim.rack_roles.create(nb_obj_dict)
                elif (model == "rack_groups"):
                    nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])

                    nb_obj = nb.dcim.rack_groups.get(name=nb_obj_dict['name'])
                    if (not nb_obj):
                        nb.dcim.rack_groups.create(nb_obj_dict)
                elif (model == "racks"):
                    nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
                    nb_obj_dict['group'] = retrieve_nb_id("dcim","rack_groups",nb_obj_dict['group'])
                    nb_obj_dict['role'] = retrieve_nb_id("dcim","rack_roles",nb_obj_dict['role'])

                    nb_obj = nb.dcim.racks.get(name=nb_obj_dict['name'])
                    if (not nb_obj):
                        nb.dcim.racks.create(nb_obj_dict)

                if (not nb_obj):
                    created_nb_count += 1

                    created_nb_objects['dcim'].append(
                        dict(
                            app="dcim",
                            model=model,
                            name=nb_obj_dict["name"],
                        )
                    )

            except pynetbox.core.query.RequestError as e:
                print(e.error)

if (created_nb_count > 0):
    print(12*"*"," The following NetBox DCIM objects have been created ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<15}{:<15}{:<20}"
    header = ("App", "Model", "Name")
    print(fmt.format(*header))

    for obj in created_nb_objects['dcim']:
        print(
            fmt.format(
                obj['app'],
                obj['model'],
                obj['name']
            )
        )
else:
    print(12*"*"," No NetBox objects were created ",12*"*")
    print("\nAll defined objects already exist")

# ndev_site = nb.dcim.sites.get(slug=row['site'])
# ndev_dtype = nb.dcim.device_types.get(slug=row['device_type'])
# ndev_drole = nb.dcim.device_roles.get(slug=row['device_role'])
# ndev_rack = nb.dcim.racks.get(q=row['rack'])
#
# # Verifies whether DCIM object exists
# if (not ndev_site):
#   created_nb_objects['site'].append(row['site'])
#   created_nb_count += 1
# if (not ndev_dtype):
#   created_nb_objects['device_type'].append(row['device_type'])
#   created_nb_count += 1
# if (not ndev_drole):
#   created_nb_objects['device_role'].append(row['device_role'])
#   created_nb_count += 1
# if (not ndev_rack):
#   created_nb_objects['rack'].append(row['rack'])
#   created_nb_count += 1



# ### Generates table of non-existent NetBox objects defined in CSV
# if ( (created_nb_count > 0) or not(flag) ):
#     # Print results of verifying duplicated IPs
#     if(not flag):
#         print()
#         print(12*"*"," Verify for duplicated IPs ",12*"*")
#         print ("One or more of the devices have duplicated IPs")
#
#     print()
#     print(12*"*"," Verify the following NetBox Objects ",12*"*")
#     print(fmt.format(*header))
#
#     # Print summary of non-existent objects in CSV
#     for model,nb_objects in created_nb_objects.items():
#         for nb_object in nb_objects:
#             print(
#                 fmt.format(
#                     model,
#                     nb_object,
#                     "Non-Existent"
#                 )
#             )
# else:
#     try:
#         # Retrieve device object by name and delete
#         for dev in nb_all_devices:
#             dev = nb.dcim.devices.get(name=dev['name'])
#             dev.delete()
#
#         # Add devices to NetBox and store resulting object in "created_devs"
#         nb_created_devices = nb.dcim.devices.create(nb_all_devices)
#
#         # Formatting and header for output
#         fmt = "{:<15}{:<20}{:<15}{:<10}{:<15}{:<25}{:<20}"
#         header = ("Device", "Dev Role", "Dev Type", "Site", "Rack", "Management Interface", "IP")
#         print()
#         print(50*"*"," Created Devices ",50*"*")
#         print(fmt.format(*header))
#
#         for created_dev in nb_created_devices:
#             # Retrieve specific interface associated w/ created device
#             nb_primary_interface = nb.dcim.interfaces.filter(device=created_dev.name,name="FastEthernet0/0")
#
#             # Create dict to store attributes for device's primary IP
#             primary_ip_addr_dict = dict(
#                 address=nb_all_devices_primaryIPs[created_dev.name],
#                 status=1,
#                 description="Management IP for {}".format(created_dev.name),
#                 interface=nb_primary_interface[0].id,
#             )
#
#             # Create primary IP and assign to device's first interface
#             new_primary_ip = nb.ipam.ip_addresses.create(primary_ip_addr_dict)
#
#             # Retrieves created device, and sets the primary IP for the device
#             dev = nb.dcim.devices.get(created_dev.id)
#             dev.primary_ip4 = new_primary_ip.id
#             dev.save()
#
#             # Print summary info for each created device
#             print(
#                 fmt.format(
#                     created_dev.name,
#                     created_dev.device_role.name,
#                     created_dev.device_type.model,
#                     created_dev.site.name,
#                     created_dev.rack.name,
#                     nb_primary_interface[0].name,
#                     new_primary_ip.address
#                 )
#             )
#
#     except pynetbox.core.query.RequestError as e:
#         print(e.error)
