#!/usr/bin/env python

import json
import xml.dom.minidom
import yaml
import xmltodict
from ncclient import manager

API_PARAMETERS = {
    "host": "ios-xe-mgmt.cisco.com",
    "port": 10000,
    "username": "developer",
    "password": "C1sco12345",
    "hostkey_verify": False,
    "allow_agent": False,
}


def create_config(nc_connection):
    """ TEST """
    print(nc_connection)

    with open("interface_data.yml", "r") as handler:
        yaml_data = yaml.safe_load(handler)

        interface_data = []
        for interface in yaml_data["interfaces_netconf"]:
            interface_data.append(
                {"name": interface["name"], "config": interface["config"]}
            )

        interfaces_to_add = {
            "config": {
                "interfaces": {
                    "@xmlns": "http://openconfig.net/yang/interfaces",
                    "interface": interface_data,
                }
            }
        }

        # print(
        #     xml.dom.minidom.parseString(
        #         xmltodict.unparse(interfaces_to_add)
        #     ).toprettyxml()
        # )

        xml_payload = xmltodict.unparse(interfaces_to_add)

        netconf_resp = nc_connection.edit_config(xml_payload, target="running")

        # Print parsed XML netconf response for debugging
        print(xml.dom.minidom.parseString(str(netconf_resp)).toprettyxml())


def get_config(nc_connection, nc_filter_query=""):
    """ TEST """

    netconf_filter = f"""
    <filter>
        {nc_filter_query}
    </filter>
    """

    netconf_resp = nc_connection.get_config(source="running", filter=netconf_filter)

    # # Print parsed XML netconf response for debugging
    # print(xml.dom.minidom.parseString(str(netconf_resp)).toprettyxml())

    parsed_data = xmltodict.parse(str(netconf_resp))
    #
    # # Print parsed dict netconf response for debugging
    # print(
    #     json.dumps(
    #         parsed_data["rpc-reply"]["data"]["interfaces"]["interface"], indent=2
    #     )
    # )
    #
    parsed_interfaces = parsed_data["rpc-reply"]["data"]["interfaces"]["interface"]

    for interface in parsed_interfaces:
        print(
            f"Interface {interface['name']} enabled state: {interface['config']['enabled']}"
        )


def delete_config(nc_connection):
    """TEST"""
    # print(nc_connection)

    with open("interface_data.yml", "r") as handler:
        yaml_data = yaml.safe_load(handler)

        interface_data = []
        for interface in yaml_data["interfaces_netconf"]:
            interface_data.append({"name": interface["name"], "@operation": "delete"})

        interfaces_to_add = {
            "config": {
                "interfaces": {
                    "@xmlns": "http://openconfig.net/yang/interfaces",
                    "interface": interface_data,
                }
            }
        }

        # print(
        #     xml.dom.minidom.parseString(
        #         xmltodict.unparse(interfaces_to_add)
        #     ).toprettyxml()
        # )

        xml_payload = xmltodict.unparse(interfaces_to_add)

        netconf_resp = nc_connection.edit_config(xml_payload, target="running")

        # Print parsed XML netconf response for debugging
        print(xml.dom.minidom.parseString(str(netconf_resp)).toprettyxml())


if __name__ == "__main__":
    with manager.connect(**API_PARAMETERS) as netconf_connection:
        print()
        # delete_config(netconf_connection)
        #
        # get_config(
        #     netconf_connection,
        #     """
        #     <interfaces xmlns="http://openconfig.net/yang/interfaces">
        #         <interface>
        #         </interface>
        #     </interfaces>
        #     """,
        # )

        # get_config(
        #     netconf_connection,
        # """
        # <interfaces xmlns="http://openconfig.net/yang/interfaces">
        #     <interface>
        #       <name>Loopback500</name>
        #     </interface>
        #     <interface>
        #       <name>Loopback501</name>
        #     </interface>
        # </interfaces>
        # """,
        # )

        # create_config(netconf_connection)
