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
    pnt_pfx = "10.10.10.0/24"
    nb_pnt_pfx = nb.ipam.prefixes.get(prefix=pnt_pfx)

    print("Free prefixes within {}:".format(pnt_pfx))
    for p in nb_pnt_pfx.available_prefixes.list():
        print("* {prefix}".format(**p))

    pfx_lengths_needed = [28,29]
    pfx_list = list()

    for i in pfx_lengths_needed:
        pfx_list.append(dict(
            prefix_length=i,
            tags=["prod","left-spine"]
        ))

    new_pfxs = nb_pnt_pfx.available_prefixes.create(pfx_list)

    field_fmt = "{:>15}: {}"
    print("Attributes of newly created prefixes (excluding non-set attributes):")
    for p in new_pfxs:
        print("Prefix {}:".format(p["prefix"]))
        for k, v in p.items():
            if not v:
                continue
            print(field_fmt.format(k, v))
        print()

except pynetbox.core.query.RequestError as e:
    print(e.error)

### Creating multiple prefixes from parent prefix
    # pnt_pfx = "10.10.10.0/24"
    # nb_pnt_pfx = nb.ipam.prefixes.get(prefix=pnt_pfx)
    #
    # print("Free prefixes within {}:".format(pnt_pfx))
    # for p in nb_pnt_pfx.available_prefixes.list():
    #     print("* {prefix}".format(**p))
    #
    # pfx_lengths_needed = [28,29]
    #
    # for i in pfx_lengths_needed:
    #     pfx_list.append(dict(
    #         prefix_length=i,
    #         tags=["prod","left-spine"]
    #     ))
    #
    # new_pfxs = nb_pnt_pfx.available_prefixes.create(pfx_list)
    #
    # field_fmt = "{:>15}: {}"
    # print("Attributes of newly created prefixes (excluding non-set attributes):")
    # for p in new_pfxs:
    #     print("Prefix {}:".format(p["prefix"]))
    #     for k, v in p.items():
    #         if not v:
    #             continue
    #         print(field_fmt.format(k, v))
    #     print()


### Creating single available prefix from parent prefix
    # pnt_pfx = "10.10.10.0/24"
    # nb_pnt_pfx = nb.ipam.prefixes.get(prefix=pnt_pfx)
    #
    # print("Free prefixes within {}:".format(pnt_pfx))
    # for p in nb_pnt_pfx.available_prefixes.list():
    #     print("* {prefix}".format(**p))
    #
    # new_pfx = nb_pnt_pfx.available_prefixes.create({"prefix_length": 25})
    #
    # field_fmt = "{:>15}: {}"
    # print("Attributes of newly created prefix (excluding non-set attributes):")
    # for k, v in new_pfx.items():
    #     if not v:
    #         continue
    #     print(field_fmt.format(k, v))
