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
from my_netbox import (create_nb_obj_dict,retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id,create_nb_log)

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
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.regions.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "sites"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.sites.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "rack_roles"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.rack_roles.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "rack_groups"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.rack_groups.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "racks"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['name'])

                                if (not nb_obj):
                                    nb.dcim.racks.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "device_roles"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.device_roles.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "manufacturers"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.manufacturers.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "platforms"):
                                nb_obj = retrieve_nb_obj(nb,"dcim",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.dcim.platforms.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))

                        if (nb_app == "ipam"):
                            if (model == "rirs"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.ipam.rirs.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "aggregates"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['prefix'])

                                if (not nb_obj):
                                    nb.ipam.aggregates.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "roles"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.ipam.roles.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "vlan_groups"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['slug'])

                                if (not nb_obj):
                                    nb.ipam.vlan_groups.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "vlans"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['vid'])

                                if (not nb_obj):
                                    nb.ipam.vlans.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "vrfs"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['name'])

                                if (not nb_obj):
                                    nb.ipam.vrfs.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))
                            elif (model == "prefixes"):
                                nb_obj = retrieve_nb_obj(nb,"ipam",model,nb_obj_dict['required_non_id']['prefix'])

                                if (not nb_obj):
                                    nb.ipam.prefixes.create(create_nb_obj_dict(nb, nb_obj_dict['required_non_id'], nb_obj_dict['required_id'], nb_obj_dict['optional_non_id'], nb_obj_dict['optional_id']))

                        if (not nb_obj):
                            created_nb_count += 1

                            created_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    nb_obj_dict['required_non_id'][retrieve_nb_identifier(model)]
                                ]
                            )
                        else:
                            existing_nb_count += 1

                            existing_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    nb_obj_dict['required_non_id'][retrieve_nb_identifier(model)]
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
