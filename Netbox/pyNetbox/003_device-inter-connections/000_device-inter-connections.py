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
from my_netbox import (retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id,retrieve_termination_obj)

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
        dev_a = retrieve_nb_obj(nb,"dcim","devices",cable_dict['dev_a'])
        dev_b = retrieve_nb_obj(nb,"dcim","devices",cable_dict['dev_b'])
        termination_a = retrieve_termination_obj(nb,cable_dict["termination_a_type"],cable_dict["dev_a"],cable_dict["termination_a"])
        termination_b = retrieve_termination_obj(nb,cable_dict["termination_b_type"],cable_dict["dev_b"],cable_dict["termination_b"])

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
