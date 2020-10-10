from genie.testbed import load
from genie.libs.conf.interface import Interface
import os

try:
    assert all(os.environ[env] for env in ['PYATS_USERNAME', 'PYATS_PASSWORD'])
except KeyError as exception:
    raise

def interfaces_current(testbed, device_name):
    device = testbed.devices[device_name]
    device.connect(learn_hostname=True, log_stdout=False)
    interfaces = device.learn("interface")

    return interfaces.info

def interface_enable_state_configure(testbed, device_name, netbox_interfaces):
    device = testbed.devices[device_name]
    device.connect(learn_hostname=True, log_stdout=False)

    for interface in netbox_interfaces:
        print(f"Setting Interface {interface.name} to enabled state {interface.enabled}")
        if (interface.name in device.interfaces.keys()):
            new_interface = device.interfaces[interface.name]
        else:
            new_interface = Interface(name = interface.name, device = device)

        new_interface.enabled = interface.enabled

        # Build and print out the configuration
        new_interface.build_config()

def interface_description_configure(testbed, device_name, netbox_interfaces):
    device = testbed.devices[device_name]
    device.connect(learn_hostname=True, log_stdout=False)

    for interface in netbox_interfaces:
        print(f"Setting Interface {interface.name} description to '{interface.description}'")
        if (interface.name in device.interfaces.keys()):
            new_interface = device.interfaces[interface.name]
        else:
            new_interface = Interface(name = interface.name, device = device)

        new_interface.description = interface.description

        # Build and print out the configuration
        new_interface.build_config()
