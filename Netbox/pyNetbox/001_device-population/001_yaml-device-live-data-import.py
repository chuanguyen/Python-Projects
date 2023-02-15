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

# Stores NetBox objects that were editted
editted_nb_count = 0
editted_nb_objects = list()

# Stores NetBox objects that are created
created_nb_count = 0
created_nb_objects = list()

interface_details = {}

# Connects to devices and parses data
# Will structure data into main dictionary of current config on devices
for device in testbed.devices:
    genie_dev = testbed.devices[device]
    genie_dev.connect(log_stdout=False)

    interface_details.update(
        {
            genie_dev.name: {
                "interfaces": dict()
            }
        }
    )

    genie_learned_interfaces = genie_dev.parse("show interfaces")
    genie_learned_interfaces_switchport = genie_dev.parse("show interfaces switchport")

    for interface, config in genie_learned_interfaces.items():

        interface_details[genie_dev.name]["interfaces"].update(
            {
                interface: dict()
            }
        )

        for config_key,config_value in config.items():

            interface_details[genie_dev.name]["interfaces"][interface].update(
                {
                    config_key: config_value
                }
            )

    for interface, config in genie_learned_interfaces_switchport.items():

        for config_key,config_value in config.items():

            interface_details[genie_dev.name]["interfaces"][interface].update(
                {
                    config_key: config_value
                }
            )


print(json.dumps(interface_details, indent=4))

try:
    # Pull all interfaces defined in NetBox for each device
    # Is a RecordSet object that can be acted on for updates
    for device in testbed.devices:
        nb_device_interfaces = list(nb.dcim.interfaces.filter(device=device))

        # Create a list hold NetBox interface names
        # Can't run list comparison operations on a NetBox RecordSet object
        nb_device_interfaces_list = list()

        for nb_device_interface in nb_device_interfaces:
            nb_device_interfaces_list.append(nb_device_interface.name)

        # Evalutes if interfaces on live device exist in NetBox object
        for interface_name, interface_attributes in interface_details[device]["interfaces"].items():
            if (interface_name in nb_device_interfaces_list):

                editted_nb_count += 1

                editted_nb_objects.append(
                    [
                        device,
                        interface_name,
                    ]
                )
            else:
                created_nb_count += 1

                created_nb_objects.append(
                    [
                        device,
                        interface_name,
                    ]
                )

        for nb_device_interface in nb_device_interfaces:
            nb_device_interface.enabled = bool(interface_details[device]["interfaces"][nb_device_interface.name].get("enabled"))
            nb_device_interface.description = interface_details[device]["interfaces"][nb_device_interface.name].get("description", "DEFAULT: No description set on device")
            nb_device_interface.mtu = interface_details[device]["interfaces"][nb_device_interface.name].get("mtu")
            nb_device_interface.duplex = interface_details[device]["interfaces"][nb_device_interface.name].get("duplex_mode")
            nb_device_interface.speed = interface_details[device]["interfaces"][nb_device_interface.name].get("bandwidth")

        print(nb_device_interfaces)

        nb.dcim.interfaces.update(nb_device_interfaces)

except pynetbox.core.query.RequestError as e:
    print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (editted_nb_count > 0):
    title = "The following NetBox objects were editted"
    headerValues = ["Device Name", "Interface"]
    nb_tools.create_nb_log(title, headerValues, editted_nb_objects, 15, 12)

if (created_nb_count > 0):
    title = "The following NetBox objects have been / need to be created"
    headerValues = ["Device Name", "Interface Name"]
    nb_tools.create_nb_log(title, headerValues, created_nb_objects, 15, 12)