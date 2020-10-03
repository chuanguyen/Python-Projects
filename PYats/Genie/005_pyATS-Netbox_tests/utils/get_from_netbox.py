import pynetbox
import os

try:
    assert all(os.environ[env] for env in ['NETBOX_TOKEN', 'NETBOX_URL'])

    netbox_token = os.getenv("NETBOX_TOKEN")
    netbox_url = os.getenv("NETBOX_URL")

    netbox = pynetbox.api(netbox_url, token=netbox_token)
except KeyError as exception:
    raise

def interfaces_sot(device_name):
    device = netbox.dcim.devices.get(name=device_name)
    interfaces = netbox.dcim.interfaces.filter(device_id=device.id)

    return interfaces
