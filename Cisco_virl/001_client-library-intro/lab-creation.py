#!/usr/bin/env python

from virl2_client import ClientLibrary
import os
import sys

try:
    assert all(os.environ[env] for env in ['VIRL_HOST', 'VIRL_USERNAME', 'VIRL_PASSWORD'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

virl_host_details = dict(virl_host = os.environ['VIRL_HOST'],
                           virl_username = os.environ['VIRL_USERNAME'],
                           virl_password = os.environ['VIRL_PASSWORD'])


def create_client_connection(virl_host, virl_username, virl_password):
    client = ClientLibrary(virl_host, virl_username, virl_password, ssl_verify=False)
    return client

if __name__ == "__main__":
    client = create_client_connection(**virl_host_details)

    ### Retrieve all labs
    # all_lab_names = [lab.title for lab in client.all_labs()]
    # print(all_lab_names)

    lab = client.create_lab("python_test_lab")

    r1 = lab.create_node("r1", "iosv", 50, 100)
    r1.config = "hostname router1"
    r2 = lab.create_node("r2", "iosv", 50, 200)
    r2.config = "hostname router2"

    # create a link between r1 and r2
    # r1_i1 = r1.create_interface()
    # r2_i1 = r2.create_interface()
    # lab_create_link(r1_i1, r2_i1)

    ### Helper function to create the interfaces and connect the nodes
    lab.connect_two_nodes(r1, r2)

    # print nodes and interfaces states:
    for node in lab.nodes():
        print(node, node.node_definition, node.image_definition)
