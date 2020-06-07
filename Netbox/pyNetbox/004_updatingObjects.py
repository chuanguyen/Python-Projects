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
    rtr = nb.dcim.devices.get(name="sw-spine-01")

    rtr_update_dict = dict(
        serial="XXXX-YYYY-ZZZZ",
        asset_tag="000-0005"
    )

    # Will apply changes in dict and save
    rtr.update(rtr_update_dict)

    rtr_modified = nb.dcim.devices.get(name="sw-spine-01")

    print("Device name: ", rtr_modified.name)
    print("New tenant: ", rtr_modified.tenant)
    print("New serial number: ", rtr_modified.serial)
    print("New asset tag: ", rtr_modified.asset_tag)

    pprint.pprint(dict(rtr))


except pynetbox.core.query.RequestError as e:
    print(e.error)


### Updating multiple attributes
    # rtr_update_dict = dict(
    #     serial="XXXX-YYYY-ZZZZ",
    #     asset_tag="000-0005"
    # )
    #
# Will apply changes in dict and save
    # rtr.update(rtr_update_dict)

### Updating individual attributes
    # rtr = nb.dcim.devices.get(name="sw-spine-01")
    # rtr.serial = ""
    # rtr.asset_tag = ""
    # rtr.save()
