#!/usr/bin/env python

from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
import json
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException


deviceList = ['192.168.10.100'
             ,'192.168.10.101'
             ,'192.168.10.102'
             ,'192.168.10.103'
             ,'192.168.10.104'
             ]

password = getpass()
driver = get_network_driver('ios')
openedDevices = []

for ip in deviceList:
    try:
        print("Connecting to "+str(ip))
        iosv = driver(ip, 'admin', password)
        iosv.open()
        openedDevices.append(iosv)
    except(AuthenticationException):
        print("Authentication failure on " + str(ip))
        continue
    except(NetMikoTimeoutException):
        print("Timeout to device " + str(ip))
        continue
    except(EOFError):
        print("End of file while attempting device " + str(ip))
        continue
    except(ConnectionException):
        print("SSH Issue. Is SSH enabled on " + str(ip))
        continue
    except Exception as unknown_error:
        print("Some other error: " + str(unknown_error))
        continue

    output = iosv.get_interfaces_ip()
    print(json.dumps(output["Vlan1"], indent=4))

for device in openedDevices:
    device.close()
