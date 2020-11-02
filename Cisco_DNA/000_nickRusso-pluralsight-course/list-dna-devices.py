#!/usr/bin/env python

import requests

dnac_url = "sandboxdnac2.cisco.com"
dnac_credentials = ("devnetuser","Cisco123!")

def create_dnac_url(dnac_path):
    url = f"https://{dnac_url}/api/v1/{dnac_path}"
    return url

def get_token():
    url = f"https://{dnac_url}/api/system/v1/auth/token"
    headers = {"Content-Type":"application/json"}
    response = requests.post(url,auth=dnac_credentials, headers=headers,verify=False)

    response.raise_for_status()
    return response.json()['Token']

def get_dnac_devices(dnac_token):
    url = create_dnac_url("network-device/")
    headers = {"Content-Type":"application/json","x-auth-token":dnac_token}
    response = requests.get(url, headers=headers,verify=False)

    response.raise_for_status()
    return response.json()['response']


if (__name__ == "__main__"):
    dnac_token = get_token()
    dnac_devices = get_dnac_devices(dnac_token)

    print("{:<30}{:<15}{:<15}".format("Hostname","IP","Family"))

    for device in dnac_devices:
        hostname = device['hostname'] or "N/A"
        family = device['family'] or "N/A"
        mgmt_ip = device['managementIpAddress'] or "N/A"
        print("{:<30}{:<15}{:<15}".format(hostname,mgmt_ip,family))
