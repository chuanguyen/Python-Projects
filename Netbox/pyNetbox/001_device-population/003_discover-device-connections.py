#!/usr/bin/env python

import sys
import os
sys.path.append(os.getcwd()+"/../modules")
import pynetbox

# Import Genie modules
from genie.conf import Genie

# Custom NB modules
import my_netbox as nb_tools

import json

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])

    NETBOX_URL = "http://localhost:8000"
    NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

    testbed = Genie.init("testbed.yaml")

except FileNotFoundError as e:
    print(f"ERROR: FILE {nb_source_file} not found", file=sys.stderr)
    raise
except KeyError as e:
    print(f"ERROR: ENVAR {e} not found", file=sys.stderr)
    sys.exit()

# Stores discovered devices / interfaces that aren't represented in Netbox
missing_nb_obj_count = 0
missing_nb_obj = list()

# Stores Netbox cables that are created
created_nb_cables_count = 0
created_nb_cables = list()

# Stores Netbox cables that don't match discovered connections
mismatched_nb_cables_count = 0
mismatched_nb_cables = list()

discovered_cdp_data = {}

for device in testbed.devices:
    genie_dev = testbed.devices[device]
    genie_dev.connect(log_stdout=False)

    discovered_cdp_data.update(
        {
            genie_dev.name: genie_dev.parse("show cdp neighbors detail")
        }
    )

try:
    for discovered_device,discovered_cdp_neighbors in discovered_cdp_data.items():
        if (discovered_cdp_neighbors["total_entries_displayed"] > 0):
            for index, learned_cdp_neighbor in discovered_cdp_neighbors["index"].items():

                dev_a_name = discovered_device
                dev_a_interface = learned_cdp_neighbor["local_interface"]
                dev_b_name = learned_cdp_neighbor["device_id"].split('.',1)[0]
                dev_b_interface = learned_cdp_neighbor["port_id"]

                # Verifies the discovered device and their connected interfaces exist in NetBox
                nb_dev_a = nb_tools.retrieve_nb_obj(nb,"dcim","devices", dev_a_name)
                nb_dev_b = nb_tools.retrieve_nb_obj(nb,"dcim","devices", dev_b_name)
                nb_dev_a_discovered_intf = nb_tools.retrieve_termination_obj(nb,"dcim.interface",dev_a_name,dev_a_interface)
                nb_dev_b_discovered_intf = nb_tools.retrieve_termination_obj(nb,"dcim.interface",dev_b_name,dev_b_interface)

                if ( (nb_dev_a and nb_dev_a_discovered_intf) and (nb_dev_b and nb_dev_b_discovered_intf) ):
                    nb_cable = nb.dcim.cables.get(device_id=[nb_dev_a.id, nb_dev_b.id])

                    if (nb_cable):

                        nb_cable_termination_a = nb_cable.a_terminations[0]
                        nb_cable_dev_a_termination_type = nb_cable.a_terminations[0].link_peers_type
                        nb_cable_termination_b = nb_cable.b_terminations[0]
                        nb_cable_dev_b_termination_type = nb_cable.b_terminations[0].link_peers_type

                        # Check if termination from returned cables match interface and type of the discovered devices
                        # Checking both cable termination A and B as those are arbitrary and the discovered device could be
                        # on either end of the NetBox cable object
                        nb_cable_termination_a_matches = ((nb_cable_termination_a.id == nb_dev_a_discovered_intf.id or nb_cable_termination_b.id == nb_dev_a_discovered_intf.id) and (nb_cable_dev_a_termination_type == "dcim.interface" or nb_cable_dev_b_termination_type == "dcim.interface"))
                        nb_cable_termination_b_matches = ((nb_cable_termination_a.id == nb_dev_b_discovered_intf.id or nb_cable_termination_b.id == nb_dev_b_discovered_intf.id) and (nb_cable_dev_a_termination_type == "dcim.interface" or nb_cable_dev_b_termination_type == "dcim.interface"))

                        # Ignores existing Netbox cable connections that match discovered connections
                        if not (nb_cable_termination_a_matches and nb_cable_termination_b_matches):
                            mismatched_nb_cables_count += 1

                            mismatched_nb_cables.append(
                                [
                                    dev_a_name,
                                    dev_a_interface,
                                    dev_b_name,
                                    dev_b_interface,
                                    nb_dev_a.name,
                                    nb_cable_termination_a.name,
                                    nb_dev_b.name,
                                    nb_cable_termination_b.name,
                                ]
                            )
                    else:
                        nb_cable_dict = dict(
                            a_terminations=[
                                dict(
                                    object_type="dcim.interface",
                                    object_id=nb_dev_a_discovered_intf.id,
                                ),
                            ],
                            b_terminations=[
                                dict(
                                    object_type="dcim.interface",
                                    object_id=nb_dev_b_discovered_intf.id,
                                ),
                            ],
                            status="connected",
                            label="Cable created from automated discovery",
                        )

                        nb.dcim.cables.create(nb_cable_dict)

                        created_nb_cables_count += 1

                        created_nb_cables.append(
                            [
                                nb_dev_a.name,
                                nb_dev_a_discovered_intf.name,
                                nb_dev_b.name,
                                nb_dev_b_discovered_intf.name,
                            ]
                        )
                else:
                    missing_nb_obj_count += 1

                    missing_nb_obj.append(
                        [
                            dev_a_name,
                            dev_a_interface,
                            dev_b_name,
                            dev_b_interface,
                        ]
                    )
except pynetbox.core.query.RequestError as e:
    print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (created_nb_cables_count > 0):
    title = "The following Netbox cables were created"
    headerValues = ["Device A", "Termination A", "Device B", "Termination B"]
    nb_tools.create_nb_log(title, headerValues, created_nb_cables, 15, 12)

if (missing_nb_obj_count > 0):
    title = "The following discovered connected devices and/or interfaces weren't found in Netbox"
    headerValues = ["Device A", "Termination A", "Device B", "Termination B"]
    nb_tools.create_nb_log(title, headerValues, missing_nb_obj, 15, 12)

if (mismatched_nb_cables_count > 0):
    title = "The following discovered connections don't match the Netbox cables"
    headerValues = ["Discovered Device A", "Discovered Termination A", "Discovered Device B", "Discovered Termination A", "Netbox Device A", "Netbox Termination A", "Netbox Device B", "Netbox Termination B"]
    nb_tools.create_nb_log(title, headerValues, mismatched_nb_cables, 7, 4)