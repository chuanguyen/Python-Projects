#!/usr/bin/env python

iosxe_hostname = "ios-xe-mgmt.cisco.com"
iosxe_netconf_port = 10000
iosxe_username = "developer"
iosxe_password = "C1sco12345"

from ncclient import manager
import xmltodict
import xml.dom.minidom

# Create an XML filter for targeted NETCONF queries
netconf_filter = """
<filter>
   <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
     <interface></interface>
   </interfaces>
</filter>"""

with manager.connect(
    host=iosxe_hostname,
    port=iosxe_netconf_port,
    username=iosxe_username,
    password=iosxe_password,
    hostkey_verify=False,
) as m:
    netconf_reply = m.get_config(source="running", filter=netconf_filter)
    # print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    interfaces = netconf_data["interfaces"]["interface"]

    for interface in interfaces:
        print(f"Interface {interface['name']} enabled status is {interface['enabled']}")


# with manager.connect(
#     host=iosxe_hostname,
#     port=iosxe_netconf_port,
#     username=iosxe_username,
#     password=iosxe_password,
#     hostkey_verify=False,
# ) as m:
#     c = m.get_config(source="running")
#     for capability in m.server_capabilities:
#         print(capability)
