#!/usr/bin/env python

from netmiko import ConnectHandler

iosv_l2_SW5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.100',
    'username': 'admin',
    'password': 'cisco',
}
iosv_l2_SW1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.101',
    'username': 'admin',
    'password': 'cisco',
}
iosv_l2_SW2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.102',
    'username': 'admin',
    'password': 'cisco',
}
iosv_l2_SW3 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.103',
    'username': 'admin',
    'password': 'cisco',
}
iosv_l2_SW4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.10.104',
    'username': 'admin',
    'password': 'cisco',
}

all_devices = [iosv_l2_SW3, iosv_l2_SW4, iosv_l2_SW2, iosv_l2_SW1, iosv_l2_SW5]

for device in all_devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('wr mem')
    print(output)
