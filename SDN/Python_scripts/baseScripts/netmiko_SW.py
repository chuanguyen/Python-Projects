#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
import json
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from simplecrypt import encrypt, decrypt
from pprint import pprint
from time import time
import csv
import threading
from multiprocessing.dummy import Pool as ThreadPool

#------------------------------------------------------- Functions
def read_devices( device_filename ):
    devices = {}

    with open ( device_filename ) as device_file:
        for device_line in device_file:

            device_info = device_line.strip().split(',')

            device = {'ipaddr': device_info[0]
                     ,'type': device_info[1]
                     ,'name': device_info[2]
                     }
            devices[device['ipaddr']] = device

    return devices

def read_device_creds( device_creds_filename, key ):

    with open( device_creds_filename, 'rb') as device_creds_file:
        device_creds_json = decrypt( key, device_creds_file.read() )

    device_creds_list = json.loads( device_creds_json.decode('utf-8'))

    # convert to dictionary of lists using dictionary comprehension
    device_creds = { dev[0]:dev for dev in device_creds_list }

    return device_creds

def config_worker( device_and_creds ):

    # For threadpool library we had to pass only one argument, so extract the two
    # pieces (device and creds) out of the one tuple passed.
    device = device_and_creds[0]
    creds  = device_and_creds[1]

    #---- Connect to the device ----
    if   device['type'] == 'junos-srx': device_type = 'juniper'
    elif device['type'] == 'cisco-ios': device_type = 'cisco_ios'
    elif device['type'] == 'cisco-xr':  device_type = 'cisco_xr'
    else:                               device_type = 'cisco_ios'    # attempt Cisco IOS as default

    print ('---- Connecting to device {0}, username={1}, password={2}'.format( device['ipaddr'],
                                                                                creds[1], creds[2] ))

    #---- Connect to the device
    session = ConnectHandler(device_type=device_type
                            ,ip=device['ipaddr']
                            ,username=creds[1]
                            ,password=creds[2]
                            )

    #session = ConnectHandler( device_type=device_type, ip='172.16.0.1',  # Faking out IP address for now
    #                                                   username=creds[1], password=creds[2] )

    # if device_type == 'juniper':
    #     #---- Use CLI command to get configuration data from device
    #     print ('---- Getting configuration from device')
    #     session.send_command('configure terminal')
    #     config_data = session.send_command('show configuration')

    if device_type == 'cisco_ios':
        #---- Use CLI command to get configuration data from device
        print ('---- Getting configuration from device')
        config_data = session.send_command('show run')

    # if device_type == 'cisco_xr':
    #     #---- Use CLI command to get configuration data from device
    #     print ('---- Getting configuration from device')
    #     config_data = session.send_command('show configuration running-config')

    #---- Write out configuration information to file
    # config_filename = 'config-' + device['ipaddr']  # Important - create unique configuration file name
    #
    # print ('---- Writing configuration: ', config_filename)
    # with open( config_filename, 'w' ) as config_out:  config_out.write( config_data )

    #---- Write out configuration information to file
    config_filename = 'config-' + device['ipaddr']  # Important - create unique configuration file name

    print ('---- Writing configuration: ', config_filename)
    with open( config_filename, 'w' ) as config_out:  config_out.write( config_data )

    session.disconnect()

    return

#------------------------------------------------------ Main

# username = input('Enter your SSH username: ')
# password = getpass()
username = "admin"
password = "cisco"

devices  = read_devices("device_list")
creds = read_device_creds("encrypted-credentials", "cisco")

# Defines the max # of threads that can be spawned,
# but prevents an excessive amount of threads from being created
while (True):
    num_threads = int(input( '\nNumber of threads (5): ' ) or '5')

    if ( num_threads < 10):
        break

config_params_list = []

starting_time = time()

print ('\n---- Begin get config sequential ------\n')

for ipaddr,device in devices.items():
    config_params_list.append( ( device, creds[ipaddr] ) )

pprint(config_params_list)

print('\n---- Creating threadpool, launching config threads ----\n')
threads = ThreadPool( num_threads )
results = threads.map( config_worker, config_params_list )

threads.close()
threads.join()


#------ Simple multi-threading ------------------------------------
#--- Issues occur when large # of devices; too many threads for local device

# for ipaddr,device in devices.items():
#     print ('Getting config for: ', device)
#     config_threads_list.append(threading.Thread( target=config_worker, args=(device, creds[ipaddr]) ))
#
# print('\n---- Begin get config threading ----\n')
#
# for config_thread in config_threads_list:
#     try:
#         config_thread.start()
#     except(AuthenticationException):
#         print("Authentication failure on " + str(ipaddr))
#         continue
#     except(NetMikoTimeoutException):
#         print("Timeout to device " + str(ipaddr))
#         continue
#     except(EOFError):
#         print("End of file while attempting device " + str(ipaddr))
#         continue
#     except(SSHException):
#         print("SSH Issue. Is SSH enabled on " + str(ipaddr))
#         continue
#     except Exception as unknown_error:
#         print("Some other error: " + str(unknown_error))
#         continue
#
# for config_thread in config_threads_list:
#     config_thread.join()

print ('\n---- End get config sequential, elapsed time=', time()-starting_time)
