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

# Stores IP addresses already assigned to devices
existing_nb_dev_IPs_count = 0
existing_nb_dev_IPs = list()

# Stores NetBox objects that are created
created_nb_objs_count = 0
created_nb_objs = list()

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
                    # Verifies whether IP has already been assigned
                    nb_existing_ip = nb.ipam.ip_addresses.get(address=interface['ipv4'][0]['prefix'])

                    if (nb_existing_ip):
                        existing_nb_dev_IPs_count += 1
                        existing_nb_dev_IPs.append(
                            dict(
                                expected_dev=dev_name,
                                expected_int=interface['name'],
                                current_dev=nb_existing_ip.interface.device.name,
                                current_int=nb_existing_ip.interface.name,
                                ip=interface['ipv4'][0]['prefix']
                            )
                        )
                    else:
                        interface_ip_dict = dict(
                            address=interface['ipv4'][0]['prefix'],
                            status=1,
                            description=interface['description'],
                            interface=dev_interface.id,
                        )

                        pprint.pprint(interface_ip_dict)
                        nb.ipam.ip_addresses.create(interface_ip_dict)

                        created_nb_objs_count += 1
                        created_nb_objs.append(
                            dict(
                                device=dev_name,
                                interface=interface['name'],
                                ip=interface['ipv4'][0]['prefix'],
                                description=interface['description']
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

if (existing_nb_dev_IPs_count > 0):
    print(12*"*"," The following IPs are already assigned ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<20}{:<20}{:<20}{:<25}{:<15}"
    header = ("Expected Device", "Expected Interface", "Current NB Device", "Current NB Interface", "IP Address")
    print(fmt.format(*header))

    for ip_address in existing_nb_dev_IPs:
        print(
            fmt.format(
                ip_address['expected_dev'],
                ip_address['expected_int'],
                ip_address['current_dev'],
                ip_address['current_int'],
                ip_address['ip']
            )
        )

if (created_nb_objs_count > 0):
    print()
    print(12*"*"," The following IPs have been assigned to the given device and interface ",12*"*")
    print()

    # Formatting and header for output
    fmt = "{:<15}{:<20}{:<20}{:<25}"
    header = ("Device", "Interface", "IP", "Description")
    print(fmt.format(*header))

    for ip in created_nb_objs:
        print(
            fmt.format(
                ip['device'],
                ip['interface'],
                ip['ip'],
                ip['description']
            )
        )

else:
    print()
    print(12*"*"," No IP addresses were assigned ",12*"*")
    print("\nAll defined IPs already exist or there were errors for some of the objects")
