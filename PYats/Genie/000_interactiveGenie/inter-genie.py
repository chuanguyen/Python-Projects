#!/usr/bin/env python

import os
import sys
from genie.testbed import load
from genie.conf.base.device import Device

# Loads testbed YAML file & verifies whether environment variables have been set

try:
    assert all(os.environ[env] for env in ['PYATS_USERNAME', 'PYATS_PASSWORD'])
except KeyError as exc:
    sys.exit(f"ERROR: missing ENVAR: {exc}")

testbed = load("empty-testbed.yaml")
print(f"Genie loaded testbed: {testbed.name}")
