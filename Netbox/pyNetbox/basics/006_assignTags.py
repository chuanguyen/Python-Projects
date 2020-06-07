#!/usr/bin/env python

import os
import sys
import pprint
from netaddr import *
import pynetbox

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

try:
    # Retrieves all devices having the same prefix in the name
    devs_to_tag = nb.dcim.devices.filter("sw-")

    for dev_to_tag in devs_to_tag:
        print("Tags currently attached to {0}: {1}".format(dev_to_tag.name, dev_to_tag.tags))

    print()

    for dev_to_tag in devs_to_tag:
        # Avoid setting tags explicitly as this overwrites existing tags
            # dev_to_tag.tags = []

        dev_to_tag.tags.extend(['prod','leaf-spine'])
        # dev_to_tag.tags = dev_to_tag.tags + ['prod','leaf-spine']
        print("Tags currently attached to {0}: {1}".format(dev_to_tag.name, dev_to_tag.tags))


except pynetbox.core.query.RequestError as e:
    print(e.error)
