#!/usr/bin/env python

iosxe_hostname = "ios-xe-mgmt.cisco.com"
iosxe_netconf_port = 10000
iosxe_username = "developer"
iosxe_password = "C1sco12345"

from ncclient import manager
import xmltodict
import xml.dom.minidom

# Create an XML configuration template for ietf-interfaces
netconf_interface_add_template = """
    <config>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
         <interface>
             <name>{name}</name>
             <description>{desc}</description>
             <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                 {type}
             </type>
             <enabled>{status}</enabled>
             <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                 <address>
                     <ip>{ip_address}</ip>
                     <netmask>{mask}</netmask>
                 </address>
             </ipv4>
         </interface>
     </interfaces>
    </config>"""

netconf_interface_delete_template = """
 <config>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
         <interface operation="delete">
             <name>{name}</name>
         </interface>
     </interfaces>
 </config>"""

# Ask for the Interface Details to Add
new_loopback = {}
new_loopback["name"] = "Loopback" + input("What loopback number to add? ")
new_loopback["desc"] = input("What description to use? ")
new_loopback["type"] = "loopback"
new_loopback["status"] = "true"
new_loopback["ip_address"] = input("What IP address? ")
new_loopback["mask"] = input("What network mask? ")

# Create the NETCONF data payload for this interface
netconf_data = netconf_interface_add_template.format(
    name=new_loopback["name"],
    desc=new_loopback["desc"],
    type=new_loopback["type"],
    status=new_loopback["status"],
    ip_address=new_loopback["ip_address"],
    mask=new_loopback["mask"],
)

print(netconf_data)

with manager.connect(
    host=iosxe_hostname,
    port=iosxe_netconf_port,
    username=iosxe_username,
    password=iosxe_password,
    hostkey_verify=False,
) as m:
    # netconf_reply = m.edit_config(netconf_data, target='running')
    print("")
