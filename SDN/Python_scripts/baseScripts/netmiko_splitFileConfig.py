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

access_devices = [iosv_l2_SW3, iosv_l2_SW4]

# Reads from the file line-by-line
with open('iosv_l2_access') as f:
    access_configs = f.read().splitlines()
print(access_configs)

for device in access_devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(access_configs)
    print(output)

core_devices = [iosv_l2_SW2, iosv_l2_SW1, iosv_l2_SW5]

with open('iosv_l2_core') as f:
    core_configs = f.read().splitlines()
print(core_configs)

for device in core_devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(core_configs)
    print(output)
