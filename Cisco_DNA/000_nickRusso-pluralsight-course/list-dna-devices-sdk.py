#!/usr/bin/env python

import requests
from dnacentersdk import DNACenterAPI
from pprint import pprint

dnac_url = "https://sandboxdnac2.cisco.com"
dnac_username = "devnetuser"
dnac_password = "Cisco123!"

if (__name__ == "__main__"):
    dnac = DNACenterAPI(username=dnac_username, password=dnac_password, base_url=dnac_url)

    dnac_devices = dnac.devices.get_device_list()
    headers = ["Hostname","IP","Family"]
    header_format = "{:<25}{:<15}{:<15}"
    print(header_format.format(*headers))

    for dnac_device in dnac_devices['response']:
        dnac_device_details = [
            dnac_device['hostname'] or "N/A",
            dnac_device['managementIpAddress'] or "N/A",
            dnac_device['family'] or "N/A"
        ]

        print(header_format.format(*dnac_device_details))
