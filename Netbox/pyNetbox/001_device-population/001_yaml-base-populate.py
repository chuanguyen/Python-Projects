#!/usr/bin/env python

import sys
import os
sys.path.append(os.getcwd()+"/../modules")

import pprint
from netaddr import *
import pynetbox
import csv
import yaml

# Custom NB modules
from my_netbox import (retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id,create_nb_log)

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

# Stores NetBox objects that are already created
existing_nb_count = 0
existing_nb_objects = list()

# Stores NetBox objects that are created
created_nb_count = 0
created_nb_objects = list()

# Cycle through creating NetBox App & Models
for nb_apps in nb_base_data:
    for nb_app,model_nb_objs in nb_apps.items():
        for model,nb_obj_dicts in model_nb_objs.items():
            for nb_obj_dict in nb_obj_dicts:
                if (nb_obj_dict):
                    nb_obj = None

                    try:
                        if (nb_app == "dcim"):
                            if (model == "regions"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])
                                if (not nb_obj):
                                    nb.dcim.regions.create(nb_obj_dict)
                            elif (model == "sites"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])
                                if (not nb_obj):
                                    # Replacing fields that require NetBox IDs as values
                                    nb_obj_dict['region'] = retrieve_nb_id(nb,"dcim","regions",nb_obj_dict['region'])
                                    nb.dcim.sites.create(nb_obj_dict)
                            elif (model == "rack_roles"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])
                                if (not nb_obj):
                                    nb.dcim.rack_roles.create(nb_obj_dict)
                            elif (model == "rack_groups"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])
                                if (not nb_obj):
                                    nb_obj_dict['site'] = retrieve_nb_id(nb,"dcim","sites",nb_obj_dict['site'])
                                    nb.dcim.rack_groups.create(nb_obj_dict)
                            elif (model == "racks"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['name'])

                                if (not nb_obj):
                                    nb_obj_dict['site'] = retrieve_nb_id(nb,"dcim","sites",nb_obj_dict['site'])
                                    nb_obj_dict['group'] = retrieve_nb_id(nb,"dcim","rack_groups",nb_obj_dict['group'])
                                    nb_obj_dict['role'] = retrieve_nb_id(nb,"dcim","rack_roles",nb_obj_dict['role'])
                                    nb.dcim.racks.create(nb_obj_dict)
                            elif (model == "device_roles"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    nb.dcim.device_roles.create(nb_obj_dict)
                            elif (model == "manufacturers"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    nb.dcim.manufacturers.create(nb_obj_dict)
                            elif (model == "platforms"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    nb_obj_dict['manufacturer'] = retrieve_nb_id(nb,"dcim","manufacturers",nb_obj_dict['manufacturer'])
                                    nb.dcim.platforms.create(nb_obj_dict)

                        if (nb_app == "ipam"):
                            if (model == "rirs"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    nb.ipam.rirs.create(nb_obj_dict)
                            elif (model == "aggregates"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['prefix'])

                                if (not nb_obj):
                                    # Replacing fields that require NetBox IDs as values
                                    nb_obj_dict['rir'] = retrieve_nb_id(nb,"ipam","rirs",nb_obj_dict['rir'])
                                    nb.ipam.aggregates.create(nb_obj_dict)
                            elif (model == "roles"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    nb.ipam.roles.create(nb_obj_dict)
                            elif (model == "vlan_groups"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['slug'])

                                if (not nb_obj):
                                    # Replacing fields that require NetBox IDs as values
                                    nb_obj_dict['site'] = retrieve_nb_id(nb,"dcim","sites",nb_obj_dict['site'])

                                    nb.ipam.vlan_groups.create(nb_obj_dict)
                            elif (model == "vlans"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['vid'])

                                if (not nb_obj):
                                    # Replacing fields that require NetBox IDs as values
                                    nb_obj_dict['site'] = retrieve_nb_id(nb,"dcim","sites",nb_obj_dict['site'])
                                    if (nb_obj_dict['group']): nb_obj_dict['group'] = retrieve_nb_id(nb,"ipam","vlan_groups",nb_obj_dict['group'])
                                    if (nb_obj_dict['role']): nb_obj_dict['role'] = retrieve_nb_id(nb,"ipam","roles",nb_obj_dict['role'])

                                    nb.ipam.vlans.create(nb_obj_dict)
                            elif (model == "vrfs"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['name'])

                                if (not nb_obj):
                                    nb.ipam.vrfs.create(nb_obj_dict)
                            elif (model == "prefixes"):
                                # Attempts to retrieves object, and creates object if it doesn't exist
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['prefix'])

                                if (not nb_obj):
                                    # Replacing fields that require NetBox IDs as values
                                    nb_obj_dict['site'] = retrieve_nb_id(nb,"dcim","sites",nb_obj_dict['site'])
                                    nb_obj_dict['role'] = retrieve_nb_id(nb,"ipam","roles",nb_obj_dict['role'])

                                    # Fields below may not always be defined, so only searches when they are defined
                                    if (nb_obj_dict['vlan']): nb_obj_dict['vlan'] = retrieve_nb_id(nb,"ipam","vlans",nb_obj_dict['vlan'])
                                    if (nb_obj_dict['vrf']): nb_obj_dict['vrf'] = retrieve_nb_id(nb,"ipam","vrfs",nb_obj_dict['vrf'])

                                    nb.ipam.prefixes.create(nb_obj_dict)

                        if (not nb_obj):
                            created_nb_count += 1

                            created_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    nb_obj_dict[retrieve_nb_identifier(model)]
                                ]
                            )
                        else:
                            existing_nb_count += 1

                            existing_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    nb_obj_dict[retrieve_nb_identifier(model)]
                                ]
                            )
                    except pynetbox.core.query.RequestError as e:
                        print(e.error)

if (existing_nb_count > 0):
    title = "The following NetBox objects already existed"
    headerValues = ["App", "Model", "Name"]
    create_nb_log(title, headerValues, existing_nb_objects, 15, 12)

if (created_nb_count > 0):
    title = "The following NetBox objects have been created"
    headerValues = ["App", "Model", "Name"]
    create_nb_log(title, headerValues, created_nb_objects, 15, 12)

else:
    print()
    print(12*"*"," No NetBox objects were created ",12*"*")
    print("\nAll defined objects already exist or there were errors for some of the objects")
