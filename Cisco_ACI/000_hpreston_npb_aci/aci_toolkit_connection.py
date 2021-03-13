#!/usr/bin/env python

from acitoolkit.acitoolkit import *

ACI_HOST = "https://10.10.20.14"
ACI_USERNAME = "admin"
ACI_PASSWORD = "C1sco12345"

aci_session = Session(ACI_HOST, ACI_USERNAME, ACI_PASSWORD)

aci_session.login()
# print(aci_session.logged_in())

aci_tenants = Tenant.get(aci_session)

for tenant in aci_tenants:
    print(tenant.name)

new_tenant = Tenant("TestTenant")

my_vrf = Context("TestVRF", new_tenant)
my_bd = BridgeDomain("TestBD", new_tenant)

print(new_tenant.get_json())
