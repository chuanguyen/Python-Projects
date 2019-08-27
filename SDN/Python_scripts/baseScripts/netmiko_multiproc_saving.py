#!/usr/bin/env python

from netmiko import ConnectHandler
import multiprocessing as mp

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

def save_config(device):
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('wr mem')
    print(output)

processes = []

for device in all_devices:
    # comma required after device to ensure it is recognized
    # as a single item tuple, rather than providing individual items to function
    processes.append(mp.Process(target=save_config, args=(device,)))

for p in processes:
    p.start()

# Meant to join all the individual procesess together to the main thread
for p in processes:
    p.join()
