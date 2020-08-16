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

    NETBOX_URL = "http://localhost:8000"
    NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

    nb_source_file = "nb_devices_interfaces.yml"

    with open(nb_source_file) as f:
        nb_base_data = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as e:
    print(f"ERROR: FILE {nb_source_file} not found", file=sys.stderr)
    raise
except KeyError as e:
    print(f"ERROR: ENVAR {e} not found", file=sys.stderr)
    sys.exit()

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
                        [
                            dev_name,
                            interface['name']
                        ]
                    )
                else:
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
                        [
                            dev_name,
                            interface['name'],
                            str(bool(interface['enabled'])),
                            str(bool(interface['mgmt_only'])),
                            interface['mode'],
                            interface['description']
                        ]
                    )

            except pynetbox.core.query.RequestError as e:
                print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (unknown_nb_dev_interfaces_count > 0):
    title = "Verify the following interfaces exist on the devices"
    headerValues = ["Device", "Interface"]
    create_nb_log(title, headerValues, unknown_nb_dev_interfaces, 5, 12)

if (configured_nb_interfaces_count > 0):
    title = "The following interfaces have been configured"
    headerValues = ["Device", "Interface","Status","Management Only","802.1Q Mode","Description"]
    create_nb_log(title, headerValues, configured_nb_interfaces, 10, 24)

else:
    print()
    print(12*"*"," No interfaces were configured ",12*"*")
    print("\nAll defined interfaces were already configured similarily or there were errors for some of the objects")
