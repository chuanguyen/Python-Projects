#!/usr/bin/env python

import os
import sys
import pprint
from netaddr import *
import pynetbox
import csv
import yaml

def retrieve_nb_obj(app, model, searchTerm):
    # Searches for a NetBox object of a given model based on a search
    # term and returns the object if it exists
    # If object can't be found, returns None
    nb_obj = None
    searchTerm_modified = None

    # Alters search term to match the slug formatting (lowercase and dashes)
    if (type(searchTerm) is str):
        searchTerm_modified = searchTerm.lower().replace(" ", "-")
    else:
        searchTerm_modified = searchTerm

    if (app == "dcim"):
        if (model == "regions"):
            nb_obj = nb.dcim.regions.get(slug=searchTerm_modified)
        elif (model == "sites"):
            nb_obj = nb.dcim.sites.get(slug=searchTerm_modified)
        elif (model == "rack_roles"):
            nb_obj = nb.dcim.rack_roles.get(slug=searchTerm_modified)
        elif (model == "rack_groups"):
            nb_obj = nb.dcim.rack_groups.get(slug=searchTerm_modified)
        elif (model == "racks"):
            nb_obj = nb.dcim.racks.get(name=searchTerm_modified)
        elif (model == "devices"):
            nb_obj = nb.dcim.devices.get(name=searchTerm)
        elif (model == "device_roles"):
            nb_obj = nb.dcim.device_roles.get(slug=searchTerm_modified)
        elif (model == "manufacturers"):
            nb_obj = nb.dcim.manufacturers.get(slug=searchTerm_modified)
        elif (model == "platforms"):
            nb_obj = nb.dcim.platforms.get(slug=searchTerm_modified)
    elif (app == "ipam"):
        if (model == "rirs"):
            nb_obj = nb.ipam.rirs.get(slug=searchTerm_modified)
        elif (model == "aggregates"):
            nb_obj = nb.ipam.aggregates.get(prefix=searchTerm_modified)
        elif (model == "roles"):
            nb_obj = nb.ipam.roles.get(slug=searchTerm_modified)
        elif (model == "prefixes"):
            nb_obj = nb.ipam.prefixes.get(prefix=searchTerm_modified)
        elif (model == "vlan_groups"):
            nb_obj = nb.ipam.vlan_groups.get(slug=searchTerm_modified)
        elif (model == "vlans"):
            nb_obj = nb.ipam.vlans.get(vid=searchTerm_modified)
        elif (model == "vrfs"):
            nb_obj = nb.ipam.vrfs.get(name=searchTeam_modified)

    return nb_obj

def retrieve_nb_identifier(model):
    # Returns human-friendly identifier for the given NetBox model

    # Stores the corresponding identifying field for the given NetBox objct
    nb_obj_name_keys = dict(
        regions="slug",
        sites="slug",
        rack_groups="slug",
        rack_roles="slug",
        racks="name",
        devices="name",
        device_roles="slug",
        manufacturers="slug",
        platforms="slug",
        rirs="slug",
        aggregates="prefix",
        roles="slug",
        prefixes="prefix",
        vlan_groups="slug",
        vlans="vid",
        vrfs="name"
    )

    return nb_obj_name_keys[model]

def retrieve_nb_id(app, model, searchTerm):
    # Searches for a NetBox object of a given model based on a search term and returns the ID
    # If object can't be found, returns the search term
    nb_obj_id = None
    nb_obj = None

    nb_obj=retrieve_nb_obj(app,model,searchTerm)

    if (nb_obj):
        nb_obj_id = nb_obj.id
        return nb_obj_id
    else:
        return searchTerm

def retrieve_termination_obj(termination_type,dev_name,termination_name):
    termination_obj = None

    if (termination_type == "dcim.interface"):
        termination_obj = nb.dcim.interfaces.get(device=dev_name,name=termination_name)
    elif (termination_type == "dcim.frontport"):
        termination_obj = nb.dcim.front_ports.get(device=dev_name,name=termination_name)
    elif (termination_type == "dcim.rearport"):
        termination_obj = nb.dcim.rear_ports.get(device=dev_name,name=termination_name)

    return termination_obj

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Read from CSV for NetBox device data
nb_source_file = "inter-connections.yml"

try:
    with open(nb_source_file) as f:
        nb_base_data = yaml.load(f, Loader=yaml.FullLoader)
except NameError as e:
    print(e)

# Stores NetBox objects that are already created
existing_nb_count = 0
existing_nb_objects = dict()

# Stores NetBox objects that are created
created_nb_count = 0
created_nb_objects = dict()

# Stores non-existent NetBox objects
nb_non_existent_count = 0
nb_non_existent_objects = dict()

try:
    for cable_dict in nb_base_data['cables']:
        dev_a = retrieve_nb_obj("dcim","devices",cable_dict['dev_a'])
        dev_b = retrieve_nb_obj("dcim","devices",cable_dict['dev_b'])
        termination_a = retrieve_termination_obj(cable_dict["termination_a_type"],cable_dict["dev_a"],cable_dict["termination_a"])
        termination_b = retrieve_termination_obj(cable_dict["termination_b_type"],cable_dict["dev_b"],cable_dict["termination_b"])

        # Need to do check whether termintation already exists

        if ( (dev_a and dev_b) and (termination_a and termination_b) ):
            nb_cable_dict = dict(
                termination_a_id=termination_a.id,
                termination_a_type=cable_dict["termination_a_type"],
                termination_b_id=termination_b.id,
                termination_b_type=cable_dict["termination_b_type"],
                type=cable_dict["type"],
                status=cable_dict["status"],
                label=cable_dict["label"],
                color=cable_dict["color"],
                length=cable_dict["length"],
                length_unit=cable_dict["length_unit"],
            )

            nb.dcim.cables.create(nb_cable_dict)
        else:
            # Have single check; present single line of the cable and indicate to verify the components
            nb_non_existent_count += 1
            print("One or both devices don't exist")
except pynetbox.core.query.RequestError as e:
    print(e.error)

#
#
# # Cycle through creating NetBox App & Models
# for apps in nb_base_data:
#     for app,model_nb_objs in apps.items():
#         for model,nb_obj_dicts in model_nb_objs.items():
#             for nb_obj_dict in nb_obj_dicts:
#                 if (nb_obj_dict):
#                     nb_obj = None
#
#                     try:
#                         if (app == "dcim"):
#                             if (model == "regions"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#                                 if (not nb_obj):
#                                     nb.dcim.regions.create(nb_obj_dict)
#                             elif (model == "sites"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#                                 if (not nb_obj):
#                                     # Replacing fields that require NetBox IDs as values
#                                     nb_obj_dict['region'] = retrieve_nb_id("dcim","regions",nb_obj_dict['region'])
#                                     nb.dcim.sites.create(nb_obj_dict)
#                             elif (model == "rack_roles"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#                                 if (not nb_obj):
#                                     nb.dcim.rack_roles.create(nb_obj_dict)
#                             elif (model == "rack_groups"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#                                 if (not nb_obj):
#                                     nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
#                                     nb.dcim.rack_groups.create(nb_obj_dict)
#                             elif (model == "racks"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['name'])
#
#                                 if (not nb_obj):
#                                     nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
#                                     nb_obj_dict['group'] = retrieve_nb_id("dcim","rack_groups",nb_obj_dict['group'])
#                                     nb_obj_dict['role'] = retrieve_nb_id("dcim","rack_roles",nb_obj_dict['role'])
#                                     nb.dcim.racks.create(nb_obj_dict)
#                             elif (model == "device_roles"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     nb.dcim.device_roles.create(nb_obj_dict)
#                             elif (model == "manufacturers"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     nb.dcim.manufacturers.create(nb_obj_dict)
#                             elif (model == "platforms"):
#                                 nb_obj = retrieve_nb_obj("dcim",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     nb_obj_dict['manufacturer'] = retrieve_nb_id("dcim","manufacturers",nb_obj_dict['manufacturer'])
#                                     nb.dcim.platforms.create(nb_obj_dict)
#
#                         if (app == "ipam"):
#                             if (model == "rirs"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     nb.ipam.rirs.create(nb_obj_dict)
#                             elif (model == "aggregates"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['prefix'])
#
#                                 if (not nb_obj):
#                                     # Replacing fields that require NetBox IDs as values
#                                     nb_obj_dict['rir'] = retrieve_nb_id("ipam","rirs",nb_obj_dict['rir'])
#                                     nb.ipam.aggregates.create(nb_obj_dict)
#                             elif (model == "roles"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     nb.ipam.roles.create(nb_obj_dict)
#                             elif (model == "vlan_groups"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['slug'])
#
#                                 if (not nb_obj):
#                                     # Replacing fields that require NetBox IDs as values
#                                     nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
#
#                                     nb.ipam.vlan_groups.create(nb_obj_dict)
#                             elif (model == "vlans"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['vid'])
#
#                                 if (not nb_obj):
#                                     # Replacing fields that require NetBox IDs as values
#                                     nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
#                                     if (nb_obj_dict['group']): nb_obj_dict['group'] = retrieve_nb_id("ipam","vlan_groups",nb_obj_dict['group'])
#                                     if (nb_obj_dict['role']): nb_obj_dict['role'] = retrieve_nb_id("ipam","roles",nb_obj_dict['role'])
#
#                                     nb.ipam.vlans.create(nb_obj_dict)
#                             elif (model == "vrfs"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['name'])
#
#                                 if (not nb_obj):
#                                     nb.ipam.vrfs.create(nb_obj_dict)
#                             elif (model == "prefixes"):
#                                 # Attempts to retrieves object, and creates object if it doesn't exist
#                                 nb_obj = retrieve_nb_obj("ipam",model,nb_obj_dict['prefix'])
#
#                                 if (not nb_obj):
#                                     # Replacing fields that require NetBox IDs as values
#                                     nb_obj_dict['site'] = retrieve_nb_id("dcim","sites",nb_obj_dict['site'])
#                                     nb_obj_dict['role'] = retrieve_nb_id("ipam","roles",nb_obj_dict['role'])
#
#                                     # Fields below may not always be defined, so only searches when they are defined
#                                     if (nb_obj_dict['vlan']): nb_obj_dict['vlan'] = retrieve_nb_id("ipam","vlans",nb_obj_dict['vlan'])
#                                     if (nb_obj_dict['vrf']): nb_obj_dict['vrf'] = retrieve_nb_id("ipam","vrfs",nb_obj_dict['vrf'])
#
#                                     nb.ipam.prefixes.create(nb_obj_dict)
#
#                         if (not nb_obj):
#                             created_nb_count += 1
#
#                             created_nb_objects[app].append(
#                                 dict(
#                                     app=app,
#                                     model=model,
#                                     name=nb_obj_dict[retrieve_nb_identifier(model)],
#                                 )
#                             )
#                         else:
#                             existing_nb_count += 1
#
#                             existing_nb_objects[app].append(
#                                 dict(
#                                     app=app,
#                                     model=model,
#                                     name=nb_obj_dict[retrieve_nb_identifier(model)],
#                                 )
#                             )
#                     except pynetbox.core.query.RequestError as e:
#                         print(e.error)
#
# if (existing_nb_count > 0):
#     print(12*"*"," The following NetBox objects already existed ",12*"*")
#     print()
#
#     # Formatting and header for output
#     fmt = "{:<15}{:<15}{:<20}"
#     header = ("App", "Model", "Name")
#     print(fmt.format(*header))
#
#     for app,model_objs in existing_nb_objects.items():
#         for obj in model_objs:
#             print(
#                 fmt.format(
#                     obj['app'],
#                     obj['model'],
#                     obj['name']
#                 )
#             )
#
#
# if (created_nb_count > 0):
#     print()
#     print(12*"*"," The following NetBox objects have been created ",12*"*")
#     print()
#
#     # Formatting and header for output
#     fmt = "{:<15}{:<15}{:<20}"
#     header = ("App", "Model", "Name")
#     print(fmt.format(*header))
#
#     for app,model_objs in created_nb_objects.items():
#         for obj in model_objs:
#             print(
#                 fmt.format(
#                     obj['app'],
#                     obj['model'],
#                     obj['name']
#                 )
#             )
#
# else:
#     print()
#     print(12*"*"," No NetBox objects were created ",12*"*")
#     print("\nAll defined objects already exist or there were errors for some of the objects")
