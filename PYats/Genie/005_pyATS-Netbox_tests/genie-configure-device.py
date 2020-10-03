#!/usr/bin/env python
from genie.conf import Genie
from genie.libs.conf.interface import Interface

import os

try:
    assert all(os.environ[env] for env in ['PYATS_USERNAME', 'PYATS_PASSWORD'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

testbed = Genie.init("testbed.yml")

device = testbed.devices['r3']
device.connect(learn_hostname=True)

interfaces = device.learn("interface")

# Create a new Interface object for the device
new_interface = Interface(name = "FastEthernet1/1", device = device)

# Configure interface properties
new_interface.description = "Genie set me!"
new_interface.enabled = True

# Build and print out the configuration
output = new_interface.build_config(apply = False)
print(output)

# Build and send the configuration to the device
output = new_interface.build_config()

# Build and print the configuration to UNCONFIG the interface
output = new_interface.build_unconfig(apply = False)
print(output)

# Build and send the UNCONFIG
output = new_interface.build_unconfig()
