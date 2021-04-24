#!/usr/bin/env python

from virl2_client import ClientLibrary
import os
import sys
import yaml

try:
    assert all(os.environ[env] for env in ['VIRL_HOST', 'VIRL_USERNAME', 'VIRL_PASSWORD'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

virl_host_details = dict(virl_host = os.environ['VIRL_HOST'],
                           virl_username = os.environ['VIRL_USERNAME'],
                           virl_password = os.environ['VIRL_PASSWORD'])

with open('virl-nodes.yml') as yaml_data:
    virl_nodes = yaml.safe_load(yaml_data)


def create_client_connection(virl_host, virl_username, virl_password):
    client = ClientLibrary(virl_host, virl_username, virl_password, ssl_verify=False)
    return client

if __name__ == "__main__":
    client = create_client_connection(**virl_host_details)
    lab = client.create_lab("demo_automated_lab")
    created_nodes = dict()


    for node, config in virl_nodes.items():
        created_node = lab.create_node(config['label'],
                                       node_definition=config['node_definition'],
                                       x=config['x'], y=config['y'])

        created_node.add_tag(config['tags'])
        created_node.config = config['config']

        for interface in config['interfaces']:
            created_node.create_interface(slot=interface['slot'])

        created_nodes[node] = created_node

    # print(created_nodes)


    #
    # # create a link between r1 and r2
    # # r1_i1 = r1.create_interface()
    # # r2_i1 = r2.create_interface()
    # # lab_create_link(r1_i1, r2_i1)
    #
    # ### Helper function to create the interfaces and connect the nodes
    # lab.connect_two_nodes(r1, r2)
