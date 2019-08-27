#!/usr/bin/env python

from napalm import get_network_driver
import json
from getpass import getpass

deviceList = ['192.168.10.100'
             ,'192.168.10.101'
             ,'192.168.10.102'
             ,'192.168.10.103'
             ,'192.168.10.104'
             ]

password = getpass()

for ip in deviceList:
    print("Connecting to "+str(ip))
    driver = get_network_driver('ios')
    iosv = driver(ip, 'admin', password)
    iosv.open()
    output = iosv.get_interfaces_ip()
    print(json.dumps(output["Vlan1"], indent=4))
    iosv.close()

# SW5_output = iosv_l2_SW5.get_interfaces_counters()
# print(json.dumps(SW5_output, indent=4))

# SW5_output = iosv_l2_SW5.get_interfaces()
# print(json.dumps(SW5_output, indent=4))
#
# # Used to output the states of each interface on a device
# for int, details in SW5_output.items():
#      print('{} : {}'.format(int, details['is_enabled']))
#
# iosv_l2_SW5.close()
