#!/usr/bin/env python

from ncclient import manager

# IOS XE Settings
ios_xe_host = "192.168.50.50"
ios_xe_port = 830
ios_xe_username = "admin"
ios_xe_password = "admin"

m = manager.connect(
    host=ios_xe_host,
    port=ios_xe_port,
    username=ios_xe_username,
    password=ios_xe_password,
    hostkey_verify=False,
    look_for_keys=False,
)

for capability in m.server_capabilities:
    print(capability)

m.close_session()
