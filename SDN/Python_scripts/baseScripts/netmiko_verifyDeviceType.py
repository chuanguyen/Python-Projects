#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
import json
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException

#username = raw_input('Enter your SSH username: ')
#password = getpass()
username = "admin"
password = "cisco"

with open('device_list') as f:
    device_list = f.read().splitlines()

for device in device_list:
    print ("Connecting to device: "+device)
    deviceIP = device

    ios_device = {
                  'device_type': 'cisco_ios'
                 ,'ip': deviceIP
                 ,'username': username
                 ,'password': password
                 }

    try:
        net_connect = ConnectHandler(**ios_device)
    except(AuthenticationException):
        print("Authentication failure on " + str(deviceIP))
        continue
    except(NetMikoTimeoutException):
        print("Timeout to device " + str(deviceIP))
        continue
    except(EOFError):
        print("End of file while attempting device " + str(deviceIP))
        continue
    except(ConnectionException):
        print("SSH Issue. Is SSH enabled on " + str(deviceIP))
        continue
    except Exception as unknown_error:
        print("Some other error: " + str(unknown_error))
        continue

    # Device types
    device_versions = ['vios_l2ADVENTERPRISEK9-M'
                      ,'VIOS-ADVENTERPRISEK9-M'
                      ,'C1900-UNIVERSALK9-M'
                      ,'C3640-IK9O3S-M'
                      ]

    # Verify software version of current device
    for software_ver in device_versions:
        print('Checking for ' + software_ver)
        output_version = net_connect.send_command('show version')
        int_version = 0
        int_version = output_version.find(software_ver)

        if (int_version > 0):
            print('Software version found: '+software_ver)
            break





# for device in devices:
#     net_connect = ConnectHandler(**device)
#     output = net_connect.send_config_set(access_configs)
#     print(output)
