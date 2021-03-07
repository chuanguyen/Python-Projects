#!/usr/bin/env python

import os
import sys
from ncclient import manager, xml_
import xmltodict
import xml.dom.minidom

# nxos_hostname = "sbx-nxos-mgmt.cisco.com"
# nxos_netconf_port = 10000
# nxos_username = "admin"
# nxos_password = "Admin_1234!"

nxos_hostname = "192.168.50.50"
nxos_netconf_port = 830
nxos_username = "admin"
nxos_password = "admin"

# Create an XML body to execute the save operation
save_body = """
<copy_running_config_src xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
     <startup-config/>
</copy_running_config_src>
"""

# Open a connection to the network device using ncclient
with manager.connect(
    host=nxos_hostname,
    port=nxos_netconf_port,
    username=nxos_username,
    password=nxos_password,
    hostkey_verify=False,
) as m:
    print("Sending a RPC operation to the device.\n")
    # Use ncclient to send the RPC operation
    # Need to convert to element tree object, or tag name error is thrown
    netconf_reply = m.dispatch(xml_.to_ele(save_body))

print("Here is the raw XML data returned from the device.\n")
# Print out the raw XML that returned
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")
