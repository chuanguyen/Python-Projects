#!/usr/bin/env python

from napalm import get_network_driver
import multiprocessing as mp
import json

# driver = get_network_driver('ios')
#
# iosv_l2_SW5 = driver('192.168.10.100', 'admin', 'cisco')
# iosv_l2_SW1 = driver('192.168.10.101', 'admin', 'cisco')
# iosv_l2_SW2 = driver('192.168.10.102', 'admin', 'cisco')
# iosv_l2_SW3 = driver('192.168.10.103', 'admin', 'cisco')
# iosv_l2_SW4 = driver('192.168.10.104', 'admin', 'cisco')

iosDev_list = ['192.168.10.100'
              ,'192.168.10.101'
              ,'192.168.10.102'
              ,'192.168.10.103'
              ,'192.168.10.104']

# all_devices = [iosv_l2_SW5,iosv_l2_SW4,iosv_l2_SW3,iosv_l2_SW2,iosv_l2_SW1]

def save_config(dev_ip):
    driver = get_network_driver('ios')
    device = driver(dev_ip, 'admin', 'cisco')
    device.open()
    deviceDetails = device.get_facts()
    output = device.cli(['wr mem'])
    print("Saving config for {}".format(deviceDetails['hostname']))
    print(output)
    device.close()

processes = []

for ip in iosDev_list:
    # comma required after device to ensure it is recognized
    # as a single item tuple, rather than providing individual items to function
    processes.append(mp.Process(target=save_config, args=(ip,)))

for p in processes:
    p.start()

# Meant to join all the individual procesess together to the main thread
for p in processes:
    p.join()
