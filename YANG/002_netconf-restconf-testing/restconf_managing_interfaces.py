#!/usr/bin/env python

import json
import yaml
import requests


API_HOST = "https://ios-xe-mgmt.cisco.com:9443/restconf"
API_CREDENTIALS = ("developer", "C1sco12345")


def main():
    """ TEST """


def create_config_merge():

    requests.packages.urllib3.disable_warnings()

    with open("interface_data.yml", "r") as handle:
        config_state = yaml.safe_load(handle)

    yang_payload = []

    # Builds a list of interfaces to be added
    for interface in config_state["interfaces_restconf"]:
        yang_payload.append(interface)

    # Data already matches structure of YANG model, so can be appended directly
    yang_config = {"openconfig-interfaces:interfaces": {"interface": yang_payload}}

    rest_headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }

    rest_reply = requests.patch(
        url=f"{API_HOST}/data/openconfig-interfaces:interfaces/",
        json=yang_config,
        headers=rest_headers,
        auth=API_CREDENTIALS,
        verify=False,
    )

    print(rest_reply.status_code)
    print(rest_reply.text)


def create_config_initial():
    requests.packages.urllib3.disable_warnings()

    with open("interface_data.yml", "r") as handle:
        config_state = yaml.safe_load(handle)

    yang_payload = []

    # Builds a list of interfaces to be added
    for interface in config_state["interfaces_restconf"]:
        yang_payload.append(interface)

    # Data already matches structure of YANG model, so can be appended directly
    yang_config = {"openconfig-interfaces:interface": yang_payload}

    rest_headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }

    rest_reply = requests.post(
        url=f"{API_HOST}/data/openconfig-interfaces:interfaces/",
        json=yang_config,
        headers=rest_headers,
        auth=API_CREDENTIALS,
        verify=False,
    )

    if rest_reply.status_code == 201:
        print("Interfaces were added successfully")
    elif rest_reply.status_code == 409:
        print("Interfaces already exist, and weren't created")
    else:
        print("An error occurred")
        print(rest_reply.text)


def get_config():
    """ TEST """
    rest_headers = dict(
        Accept="application/yang-data+json, application/yang-data.errors+json"
    )

    rest_reply = requests.get(
        url=f"{API_HOST}/data/openconfig-interfaces:interfaces",
        headers=rest_headers,
        auth=API_CREDENTIALS,
        verify=False,
    )

    ### Uncomment to show returned response object
    # print(json.dumps(rest_reply.json(), indent=2))

    interfaces = rest_reply.json()

    for interface in interfaces["openconfig-interfaces:interfaces"]["interface"]:
        print(
            f"Interface: {interface['config']['name']}, Description: {interface['config']['description']}, Enabled: {interface['config']['enabled']}"
        )


if __name__ == "__main__":
    main()
