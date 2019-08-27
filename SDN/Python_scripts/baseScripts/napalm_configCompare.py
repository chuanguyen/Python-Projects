#!/usr/bin/env python

from napalm import get_network_driver
import json

driver = get_network_driver('ios')

iosv_l2_SW5 = driver('192.168.10.100', 'admin', 'cisco')
iosv_l2_SW1 = driver('192.168.10.101', 'admin', 'cisco')
iosv_l2_SW2 = driver('192.168.10.102', 'admin', 'cisco')
iosv_l2_SW3 = driver('192.168.10.103', 'admin', 'cisco')
iosv_l2_SW4 = driver('192.168.10.104', 'admin', 'cisco')

all_devices = [iosv_l2_SW5,iosv_l2_SW4,iosv_l2_SW3,iosv_l2_SW2,iosv_l2_SW1]

iosv_l2_SW5.open()

print("Configuring ACLs")
# Consider that scp must be enabled on the IOS devices prior
# Otherwise, an exception will be raised
iosv_l2_SW5.load_merge_candidate(filename='ACL1.cfg')

# Compares against the above loaded config that
# Is not yet committed to the network device
# Compares line by line in loaded config to running-config
# Will only execute the lines that differ
diffs = iosv_l2_SW5.compare_config()

if len(diffs) > 0:
    # Outputs the differing lines btwn the existing config and loaded config
    print(diffs)
    # iosv_l2_SW5.commit_config()
else:
    print('No changes necessary')
    iosv_l2_SW5.discard_config()

iosv_l2_SW5.close()
