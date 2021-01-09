#!/bin/bash
# Script to generate tree-structure of YANG modules

# Build OC interfaces tree
pyang --format tree --path oc-yang \
  oc-yang/release/models/interfaces/openconfig-interfaces.yang \
  > oc-yang-interfaces.txt

# Build OC Ethernet interface specific tree
pyang --format tree --path oc-yang \
  oc-yang/release/models/interfaces/openconfig-if-ethernet.yang \
  > oc-yang-ethernet-interfaces.txt

# Build OC VLAN specific tree
pyang --format tree --path oc-yang \
  oc-yang/release/models/vlan/openconfig-vlan.yang \
  > oc-yang-vlans.txt

# Build Cisco IOS-XE DHCP specific tree
pyang --format tree --path industry-yang/ \
  --lax-quote-checks industry-yang/vendor/cisco/xe/16111/Cisco-IOS-XE-dhcp.yang \
  > ios-xe-dhcp.tx
