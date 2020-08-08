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
from my_netbox import (retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id)

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
                            interface['untagged_vlan'] = retrieve_nb_id(nb, "ipam", "vlans", interface['untagged_vlan'])

                        if (interface['tagged_vlans']):
                            # Stores list of IDs of tagged vlans defined for interface
                            tagged_vlan_id_list = list()

                            for tagged_vlan in interface['tagged_vlans']:
                                tagged_vlan_id_list.append(
                                    retrieve_nb_id(nb, "ipam", "vlans", tagged_vlan)
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
