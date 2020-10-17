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
import my_netbox as nb_tools

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])

    NETBOX_URL = "http://localhost:8000"
    NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

    nb_source_file = "base_nb_objects.yml"

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

# Cycle through creating NetBox App & Models
for nb_apps in nb_base_data:
    for nb_app,model_nb_objs in nb_apps.items():
        for model,obj_dicts in model_nb_objs.items():
            for obj_dict in obj_dicts:
                if (obj_dict):
                    nb_obj = None

                    try:
                        # Verifies if the defined device already exists
                        nb_obj = nb_tools.retrieve_nb_obj(nb, nb_app, model,obj_dict['required_non_id'][nb_tools.retrieve_nb_identifier(model)] )

                        if (not nb_obj):
                            nb_obj_dict = nb_tools.create_nb_obj_dict(nb, obj_dict['required_non_id'], obj_dict['required_id'],obj_dict['optional_non_id'], obj_dict['optional_id'])

                            nb_tools.create_nb_obj(nb, nb_app, model, nb_obj_dict)

                            created_nb_count += 1

                            created_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    obj_dict['required_non_id'][nb_tools.retrieve_nb_identifier(model)]
                                ]
                            )
                        else:
                            existing_nb_count += 1

                            existing_nb_objects.append(
                                [
                                    nb_app,
                                    model,
                                    obj_dict['required_non_id'][nb_tools.retrieve_nb_identifier(model)]
                                ]
                            )
                    except pynetbox.core.query.RequestError as e:
                        print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (existing_nb_count > 0):
    title = "The following NetBox objects already existed"
    headerValues = ["App", "Model", "Name"]
    nb_tools.create_nb_log(title, headerValues, existing_nb_objects, 15, 12)

if (created_nb_count > 0):
    title = "The following NetBox objects have been created"
    headerValues = ["App", "Model", "Name"]
    nb_tools.create_nb_log(title, headerValues, created_nb_objects, 15, 12)

else:
    print()
    print(12*"*"," No NetBox objects were created ",12*"*")
    print("\nAll defined objects already exist or there were errors for some of the objects")
