#!/usr/bin/env python

"""

Rather than relying on static testbed files and building manually, can dynamically
generate the testbed file from a list of devices (ie. CSV, etc)

"""

import os
import sys
import yaml
from genie.testbed import load
from genie.conf.base.device import Device

# Loads testbed YAML file & verifies whether environment variables have been set

try:
    assert all(os.environ[env] for env in ['PYATS_USERNAME', 'PYATS_PASSWORD'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

#testbed = load("empty-testbed.yaml")
testbed = load("Generated_testbed.yaml")
print(f"Genie loaded testbed: {testbed.name}")

def add_device(hostname, os_type, testbed, device_type='switch', ip_addr=None, log_stdout=False):
    """
    This function will create a Device instance and initiate the connection
    with log_stdout disabled by default.  If the device already exists and is
    connected then this function will return what already exists.
    Examples
    --------
        dev = add_device('switch1', 'nxos', testbed)
        dev.parse('show version')
    Parameters
    ----------
    hostname : str
        The hostname of the device
    os_type : str
        The OS type of the device.  Must be one of the values listed on the docs website:
        https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html#manage-connections
    testbed : Testbed
        The testbed attributed from the loaded testbed file
    device_type : str
        User device device-type string
    ip_addr : str
        Optional.  The IP address for the hostname.  If given, this value will
        be used to open the connection.  If not given, then the `hostname`
        parameter must be in DNS.
    log_stdout : bool
        Optional, default=False.  Controls the initial connection setting to
        disable/enable stdout logging.
    Returns
    -------
    Device
        Connected device instance
    """

    # see if the device already exists and is connected.  If it is, then return
    # what we have, otherwise proceed to create a new device and connect.

    has_device = testbed.devices.get(hostname)
    if has_device:
        if has_device.is_connected():
            return has_device
        else:
            del testbed.devices[hostname]

    dev = Device(hostname,
                 os=os_type,  # required
                 type=device_type,  # optional

                 # genie uses the 'custom' field to select parsers by os_type

                 custom={'abstraction': {'order': ['os']}},

                 # connect only using SSH, prevent genie from making config
                 # changes to the device during the login process.

                 connections=make_ssh_conn(ip_addr or hostname))

    testbed.add_device(dev)

    return dev

def make_ssh_conn(hostname):
    """
    This function creates a connections dict used when creating a new Device
    instance.  The returned dict will only contain an SSH connection.  For more
    details on connection schema, see this doc:
    https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html#production-yaml-schema
    Parameters
    ----------
    hostname : str
        The DNS hostname or IP address to connect to the device.
    Returns
    -------
    dict
    """
    return {'default': dict(host=hostname,
                            arguments=dict(init_config_commands=[],
                                           init_exec_commands=[]),
                            protocol='ssh')}
