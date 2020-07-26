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

# Stores NetBox objects that are created
configured_nb_interfaces_count = 0
configured_nb_interfaces = list()

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
                    # Code to configure interfaces
                    ## Can make changes without verification
                    ## Netbox change log can be used to track history
                    nb_interface_config_dict = dict(
                        type=interface['type'],
                        description=interface['description'],
                        enabled=interface['enabled'],
                        mac_address=interface['mac_address'],
                        mgmt_only=interface['mgmt_only'],
                    )

                    # Verifies if mode is defined, which indicates if VLANs are specified
                    if (interface['mode']):
                        if (interface['untagged_vlan']):
                            interface['untagged_vlan'] = retrieve_nb_id("ipam", "vlans", interface['untagged_vlan'])

                        if (interface['tagged_vlans']):
                            # Stores list of IDs of tagged vlans defined for interface
                            tagged_vlan_id_list = list()

                            for tagged_vlan in interface['tagged_vlans']:
                                tagged_vlan_id_list.append(
                                    retrieve_nb_id("ipam", "vlans", tagged_vlan)
                                )
                            interface['tagged_vlans'] = tagged_vlan_id_list

                        if (interface['mode'] == "access"):
                            nb_interface_config_dict.update(
                                mode=interface['mode'],
                                untagged_vlan=interface['untagged_vlan'],
                            )
                        else:
                            nb_interface_config_dict.update(
                                mode=interface['mode'],
                                untagged_vlan=interface['untagged_vlan'],
                                tagged_vlans=interface['tagged_vlans'],
                            )

                    dev_interface.update(nb_interface_config_dict)

                    configured_nb_interfaces_count += 1
                    configured_nb_interfaces.append(
                        dict(
                            device=dev_name,
                            interface=interface['name'],
                            description=interface['description'],
                            enabled=interface['enabled'],
                            mgmt_only=interface['mgmt_only'],
                            mode=interface['mode'],
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

if (configured_nb_interfaces_count > 0):
    print()
    print(12*"*"," The following interfaces have been configured ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<15}{:<20}{:<25}{:<10}{:<20}{:<20}"
    header = ("Device", "Interface", "Description","Status","Management Only","802.1Q Mode")
    print(fmt.format(*header))

    for interface in configured_nb_interfaces:
        print(
            fmt.format(
                interface['device'],
                interface['interface'],
                interface['description'],
                str(bool(interface['enabled'])),
                str(bool(interface['mgmt_only'])),
                interface['mode'] or "",
            )
        )

else:
    print()
    print(12*"*"," No interfaces were configured ",12*"*")
    print("\nAll defined interfaces were already configured similarily or there were errors for some of the objects")
