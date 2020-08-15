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
from my_netbox import (retrieve_nb_obj,retrieve_nb_identifier,retrieve_nb_id,create_nb_log)

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN'])
except KeyError as exc:
    print(f"ERROR: ENVAR {e} not found", file=sys.stderr)
    sys.exit()

NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = os.environ['NETBOX_TOKEN']

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

### Read from CSV for NetBox device data
nb_source_file = "nb_devices.csv"

# Stores info on created NB devices
nb_all_created_devices_count = 0
nb_all_created_devices = list()

# Stores all already created NetBox objects
nb_existing_devices_count = 0
nb_existing_devices = list()

# Stores non-existent NetBox objects
nb_non_existent_devices_count = 0
nb_non_existent_devices = list()

# Stores devices and attributes that will be created
nb_all_devices = list()
nb_all_devices_primaryIPs = dict()
nb_all_devices_mgmt_intf = dict()

# Stores IPs for duplicate checking
all_IPs = list()
unique_IPs = set()
duplicated_IPs = list()

try:
    with open(nb_source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
          nb_obj = None

          ndev_site = retrieve_nb_obj(nb,"dcim","sites",row['site'])
          ndev_rack = retrieve_nb_obj(nb,"dcim","racks",row['rack'])
          ndev_dtype = retrieve_nb_obj(nb,"dcim","device_types",row['device_type'])
          ndev_drole = retrieve_nb_obj(nb,"dcim","device_roles",row['device_role'])
          ndev_platform = retrieve_nb_obj(nb,"dcim","platforms",row['platform'])

          # Verifies whether DCIM object exists
          if (not (ndev_site and ndev_dtype and ndev_drole and ndev_rack and ndev_platform) ):
              nb_non_existent_devices_count += 1

              nb_non_existent_devices.append(
                [
                    row['name'],
                    row['site'],
                    row['rack'],
                    row['device_type'],
                    row['device_role'],
                    row['platform']
                ]
              )

          # Generates dict of values for PyNetbox to create object
          if (nb_non_existent_devices_count == 0):
              nb_obj = nb.dcim.devices.get(name=row['name'])

              # Adds primary IPs to list for duplicate checking
              all_IPs.append(row['primary_ipv4'])

              if (not nb_obj):
                  nb_all_created_devices_count += 1

                  nb_all_devices.append(
                    dict(
                        name=row['name'],
                        site=ndev_site.id,
                        platform=ndev_platform.id,
                        device_type=ndev_dtype.id,
                        device_role=ndev_drole.id,
                        rack=ndev_rack.id,
                        face=row['face'],
                        position=row['position'],
                        serial=row['serial'],
                        asset_tag=row['asset_tag'],
                        status=row['status'],
                    )
                  )

                  nb_all_created_devices.append(
                    [
                        row['name'],
                        row['device_type'],
                        row['site'],
                        row['rack'],
                        row['mgmt_intf'],
                        row['primary_ipv4']
                    ]
                  )

                  nb_all_devices_primaryIPs[row['name']] = row['primary_ipv4']
                  nb_all_devices_mgmt_intf[row['name']] = row['mgmt_intf']
              else:
                  nb_existing_devices_count += 1

                  nb_existing_devices.append(
                      [
                          nb_obj.name,
                          nb_obj.site.name,
                          nb_obj.rack.name,
                          nb_obj.serial,
                          nb_obj.asset_tag,
                          nb_obj.status.label
                      ]
                  )


except FileNotFoundError as e:
    print(f"ERROR: File {nb_source_file} not found", file=sys.stderr)
except pynetbox.core.query.RequestError as e:
    print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)

if (nb_existing_devices_count > 0):
    title = "The following NetBox devices already exist"
    headerValues = ["Name", "Site", "Rack", "Serial #", "Asset Tag", "Status"]
    create_nb_log(title, headerValues, nb_existing_devices, 15, 36)

### Generates table of non-existent NetBox objects defined in CSV
if ( nb_non_existent_devices_count > 0 ):
    title = "One or more of the following device attributes are invalid"
    headerValues = ["Name", "Site", "Rack", "Device Type", "Device Role", "Platform"]
    create_nb_log(title, headerValues, nb_non_existent_devices, 15, 30)

# Creates a set to remove duplicate IPs
# If length of set differs from list, indicates there are duplicate IPs
flag = len(set(all_IPs)) == len(all_IPs)

# Print results of verifying duplicated IPs
if(not flag):
    for device_ip in all_IPs:
        if (device_ip not in unique_IPs):
            unique_IPs.add(device_ip)
        else:
            duplicated_IPs.append([device_ip,])

    title = "The following IPs are duplicated"
    headerValues = ["Duplicated IP Addresses"]
    create_nb_log(title, headerValues, duplicated_IPs, 15, 12)

elif (nb_all_created_devices_count > 0):
    try:
        # Add devices to NetBox and store resulting object in "created_devs"
        nb_created_devices = nb.dcim.devices.create(nb_all_devices)

        for created_dev in nb_created_devices:
            # Retrieve specific interface associated w/ created device
            nb_primary_interface = nb.dcim.interfaces.filter(device=created_dev.name,name=nb_all_devices_mgmt_intf[created_dev.name])

            # Create dict to store attributes for device's primary IP
            primary_ip_addr_dict = dict(
                address=nb_all_devices_primaryIPs[created_dev.name],
                status=1,
                description=f"Management IP for {created_dev.name}",
                interface=nb_primary_interface[0].id,
            )

            # Create primary IP and assign to device's first interface
            new_primary_ip = nb.ipam.ip_addresses.create(primary_ip_addr_dict)

            # Retrieves created device, and sets the primary IP for the device
            dev = nb.dcim.devices.get(created_dev.id)
            dev.primary_ip4 = new_primary_ip.id
            dev.save()

            title = "The following NetBox objects were created"
            headerValues = ["Device", "Type", "Site", "Rack", "Management Interface", "IP"]
            create_nb_log(title, headerValues, nb_all_created_devices, 10, 36)

    except pynetbox.core.query.RequestError as e:
        print(f"ERROR: NetBox query request failed {e}", file=sys.stderr)
else:
    print()
    print(24*"*"," No NetBox devices were created ",24*"*")
    print("\nAll defined devices already exist or there were errors for some of the objects")
