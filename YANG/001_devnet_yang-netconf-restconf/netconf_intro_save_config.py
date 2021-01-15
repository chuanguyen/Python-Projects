#!/usr/bin/env python

iosxe_hostname = "ios-xe-mgmt.cisco.com"
iosxe_netconf_port = 10000
iosxe_username = "developer"
iosxe_password = "C1sco12345"

from ncclient import manager, xml_
import xmltodict
import xml.dom.minidom

save_body = """
 <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
 """

with manager.connect(
    host=iosxe_hostname,
    port=iosxe_netconf_port,
    username=iosxe_username,
    password=iosxe_password,
    hostkey_verify=False,
) as m:
    print("")
