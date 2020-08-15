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
from my_netbox import (retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id,retrieve_termination_obj,create_nb_log)

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])

    NETBOX_URL = "http://localhost:8000"
    NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

    nb_source_file = "inter-connections.yml"

    with open(nb_source_file) as f:
        nb_base_data = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as e:
    print(f"ERROR: FILE {nb_source_file} not found", file=sys.stderr)
    raise
except KeyError as e:
    print(f"ERROR: ENVAR {e} not found", file=sys.stderr)
    sys.exit()

# Stores NetBox objects that are already created
existing_nb_count = 0
existing_nb_objects = list()

# Stores NetBox objects that are created
created_nb_count = 0
created_nb_objects = list()

# Stores non-existent NetBox objects
nb_non_existent_count = 0
nb_non_existent_objects = list()

try:
    for cable_dict in nb_base_data['cables']:
        nb_dev_a = retrieve_nb_obj(nb,"dcim","devices",cable_dict['dev_a'])
        nb_dev_b = retrieve_nb_obj(nb,"dcim","devices",cable_dict['dev_b'])
        nb_termination_a = retrieve_termination_obj(nb,cable_dict["termination_a_type"],cable_dict["dev_a"],cable_dict["termination_a"])
        nb_termination_b = retrieve_termination_obj(nb,cable_dict["termination_b_type"],cable_dict["dev_b"],cable_dict["termination_b"])

        if ( (nb_dev_a and nb_termination_a) and (nb_dev_b and nb_termination_b) ):
            nb_cable = None

            # With cables, unable to search from both ends using NetBox API
            # Queries are only from the perspective from one end
            # Must retrieve cables from a given device. Returned object has info on both ends
            # Must then manually sift through through cables and verify the interface IDs from the returned object
            nb_cables_search = nb.dcim.cables.filter(device_id=nb_dev_a.id)

            # Check if termination A & B from returned cables match interface and type
            for nb_cable_search in nb_cables_search:
                if ((nb_cable_search.termination_a_id == nb_termination_a.id and nb_cable_search.termination_a_type == cable_dict["termination_a_type"]) and (nb_cable_search.termination_b_id == nb_termination_b.id and nb_cable_search.termination_b_type == cable_dict["termination_b_type"])):
                    nb_cable = nb_cable_search

            if (nb_cable):
                existing_nb_count += 1

                existing_nb_objects.append(
                    [
                        nb_cable.termination_a.device.name,
                        nb_cable.termination_a.name,
                        nb_cable.termination_a_type,
                        nb_cable.termination_b.device.name,
                        nb_cable.termination_b.name,
                        nb_cable.termination_b_type,
                        nb_cable.type,
                        nb_cable.status.label
                    ]
                )
            else:
                nb_cable_dict = dict(
                    termination_a_id=nb_termination_a.id,
                    termination_a_type=cable_dict["termination_a_type"],
                    termination_b_id=nb_termination_b.id,
                    termination_b_type=cable_dict["termination_b_type"],
                    type=cable_dict["type"],
                    status=cable_dict["status"],
                    label=cable_dict["label"],
                    color=cable_dict["color"],
                    length=cable_dict["length"],
                    length_unit=cable_dict["length_unit"],
                )

                nb.dcim.cables.create(nb_cable_dict)

                created_nb_count += 1
                created_nb_objects.append(
                    [
                        cable_dict['dev_a'],
                        cable_dict['termination_a'],
                        cable_dict['termination_a_type'],
                        cable_dict['dev_b'],
                        cable_dict['termination_b'],
                        cable_dict['termination_b_type'],
                        cable_dict['type'],
                        cable_dict['status']
                    ]
                )
        else:
            nb_non_existent_count += 1
            nb_non_existent_objects.append(
                [
                    cable_dict["dev_a"],
                    cable_dict["termination_a"],
                    cable_dict['termination_a_type'],
                    cable_dict["dev_b"],
                    cable_dict["termination_b"],
                    cable_dict['termination_b_type']
                ]
            )
except pynetbox.core.query.RequestError:
    print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (nb_non_existent_count > 0):
    title = "One or more components of the following cable(s) doesn't exist"
    headerValues = ["Device A", "Termination A", "Termination A Type", "Dev B", "Termination B", "Termination B Type"]
    create_nb_log(title, headerValues, nb_non_existent_objects, 5, 24)

if (existing_nb_count > 0):
    title = "The following NetBox cables already exist"
    headerValues = ["Device A", "Termination A", "Termination A Type", "Dev B", "Termination B", "Termination B Type","Type","Status"]
    create_nb_log(title, headerValues, existing_nb_objects, 5, 30)

if (created_nb_count > 0):
    title = "The following NetBox cables were created"
    headerValues = ["Device A", "Termination A", "Termination A Type", "Dev B", "Termination B", "Termination B Type", "Type", "Status"]
    create_nb_log(title, headerValues, created_nb_objects, 5, 42)
else:
    print()
    print(32*"*"," No cables were created ",32*"*")
    print("\nAll defined cables were already configured or there were errors for some of the objects")
