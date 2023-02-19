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

assert all(os.environ[env] for env in ['NETBOX_TOKEN'])

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

testbed = Genie.init("testbed.yaml")

genie_dev = testbed.devices["IOU1"]
genie_dev.connect(log_stdout=False)

genie_learned_cdp_neighbors_detail = genie_dev.parse("show cdp neighbors detail")

# print(json.dumps(genie_learned_cdp_neighbors_detail, indent=4))

if (genie_learned_cdp_neighbors_detail["total_entries_displayed"] > 0):
    for index, learned_cdp_neighbor in genie_learned_cdp_neighbors_detail["index"].items():

        dev_a_name = genie_dev.name
        dev_a_interface = learned_cdp_neighbor["local_interface"]
        dev_b_name = learned_cdp_neighbor["device_id"].split('.',1)[0]
        dev_b_interface = learned_cdp_neighbor["port_id"]

        # Verifies the discovered device and their connected interfaces exist in NetBox
        nb_dev_a = nb_tools.retrieve_nb_obj(nb,"dcim","devices", dev_a_name)
        nb_dev_b = nb_tools.retrieve_nb_obj(nb,"dcim","devices", dev_b_name)
        nb_termination_a = nb_tools.retrieve_termination_obj(nb,"dcim.interface",dev_a_name,dev_a_interface)
        nb_termination_b = nb_tools.retrieve_termination_obj(nb,"dcim.interface",dev_b_name,dev_b_interface)

        if ( (nb_dev_a and nb_termination_a) and (nb_dev_b and nb_termination_b) ):
            nb_cable = nb.dcim.cables.get(device_id=[nb_dev_a.id, nb_dev_b.id])

            nb_cable_dev_a_id = nb_cable.a_terminations[0].id
            nb_cable_dev_a_termination_type = nb_cable.a_terminations[0].link_peers_type
            nb_cable_dev_b_id = nb_cable.b_terminations[0].id
            nb_cable_dev_b_termination_type = nb_cable.b_terminations[0].link_peers_type

            # Check if termination from returned cables match interface and type of the discovered devices
            # Checking both cable termination A and B as those are arbitrary and the discovered device could be
            # on either end of the NetBox cable object
            nb_cable_termination_a_matches = ((nb_cable_dev_a_id == nb_termination_a.id or nb_cable_dev_b_id == nb_termination_a.id) and (nb_cable_dev_a_termination_type == "dcim.interface" or nb_cable_dev_b_termination_type == "dcim.interface"))
            nb_cable_termination_b_matches = ((nb_cable_dev_a_id == nb_termination_b.id or nb_cable_dev_b_id == nb_termination_b.id) and (nb_cable_dev_a_termination_type == "dcim.interface" or nb_cable_dev_b_termination_type == "dcim.interface"))

            if ( nb_cable_termination_a_matches and nb_cable_termination_b_matches):
                print(f"interconnect exists between {dev_a_name} and {dev_b_name}")