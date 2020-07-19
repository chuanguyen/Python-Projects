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

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Read from CSV for NetBox device data
nb_source_file = "nb_devices_interfaces.yml"

try:
    with open(nb_source_file) as f:
        nb_base_data = yaml.load(f, Loader=yaml.FullLoader)
except NameError as e:
    print(e)

# Stores references to non-existent or unrecognized interfaces on NB devices
unknown_nb_dev_interfaces_count = 0
unknown_nb_dev_interfaces = list()

# Stores IP addresses already assigned to devices
existing_nb_dev_IPs_count = 0
existing_nb_dev_IPs = list()

# Stores NetBox objects that are created
created_nb_IPs_count = 0
created_nb_IPs = list()

# Cycle through assiging IPs to NB Device Interfaces
for dev in nb_base_data['devices']:
    for dev_name,interfaces in dev.items():
        for interface in interfaces:
            try:
                dev_interface = nb.dcim.interfaces.get(device=dev_name,name=interface['name'])

                if (not dev_interface):
                    unknown_nb_dev_interfaces_count += 1
                    unknown_nb_dev_interfaces.append(
                        dict(
                            device=dev_name,
                            name=interface['name'],
                        )
                    )
                else:
                    # Verifies whether IP has already been assigned
                    nb_existing_ip = nb.ipam.ip_addresses.get(address=interface['ipv4'][0]['prefix'])

                    if (nb_existing_ip):
                        existing_nb_dev_IPs_count += 1
                        existing_nb_dev_IPs.append(
                            dict(
                                expected_dev=dev_name,
                                expected_int=interface['name'],
                                current_dev=nb_existing_ip.interface.device.name,
                                current_int=nb_existing_ip.interface.name,
                                ip=interface['ipv4'][0]['prefix']
                            )
                        )
                    else:
                        # Verify some of the fields exist if defined
                        # VLANs, Roles, etc

                        interface_ip_dict = dict(
                            address=interface['ipv4'][0]['prefix'],
                            status=1,
                            description=interface['description'],
                            interface=dev_interface.id,
                        )

                        nb.ipam.ip_addresses.create(interface_ip_dict)

                        created_nb_IPs_count += 1
                        created_nb_IPs.append(
                            dict(
                                device=dev_name,
                                interface=interface['name'],
                                ip=interface['ipv4'][0]['prefix'],
                                description=interface['description']
                            )
                        )
            except pynetbox.core.query.RequestError as e:
                print(e.error)

if (unknown_nb_dev_interfaces_count > 0):
    print(12*"*"," Verify the following interfaces exist on the devices ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<15}{:<15}"
    header = ("Device", "Interface")
    print(fmt.format(*header))

    for interface in unknown_nb_dev_interfaces:
        print(
            fmt.format(
                interface['device'],
                interface['name']
            )
        )

if (existing_nb_dev_IPs_count > 0):
    print(12*"*"," The following IPs are already assigned ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<20}{:<20}{:<20}{:<25}{:<15}"
    header = ("Expected Device", "Expected Interface", "Current NB Device", "Current NB Interface", "IP Address")
    print(fmt.format(*header))

    for ip_address in existing_nb_dev_IPs:
        print(
            fmt.format(
                ip_address['expected_dev'],
                ip_address['expected_int'],
                ip_address['current_dev'],
                ip_address['current_int'],
                ip_address['ip']
            )
        )

if (created_nb_IPs_count > 0):
    print()
    print(12*"*"," The following IPs have been assigned to the given device and interface ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<15}{:<20}{:<15}{:<25}"
    header = ("Device", "Interface", "IP", "Description")
    print(fmt.format(*header))

    for ip in created_nb_IPs:
        print(
            fmt.format(
                ip['device'],
                ip['interface'],
                ip['ip'],
                ip['description']
            )
        )

else:
    print()
    print(12*"*"," No IP addresses were assigned ",12*"*")
    print("\nAll defined IPs already exist or there were errors for some of the objects")
