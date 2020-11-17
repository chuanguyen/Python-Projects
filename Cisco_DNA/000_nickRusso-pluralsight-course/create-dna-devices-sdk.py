#!/usr/bin/env python

import requests
from dnacentersdk import DNACenterAPI
from pprint import pprint

dnac_url = "https://sandboxdnac2.cisco.com"
dnac_username = "devnetuser"
dnac_password = "Cisco123!"

if (__name__ == "__main__"):
    dnac = DNACenterAPI(username=dnac_username, password=dnac_password, base_url=dnac_url)

    dnac_new_device_properties = {
        "cliTransport": "ssh",
        "enablePassword": "secret456!",
        "ipAddress": ["192.0.2.1"],
        "password": "secret123!",
        "snmpVersion": "v2",
        "snmpROCommunity": "readonly",
        "snmpRWCommunity": "readwrite",
        "snmpRetry": 1,
        "snmpTimeout": 60,
        "userName": "calvin",
        "snmpAuthPassphrase": "",
        "snmpAuthProtocol": "",
        "snmpMode": "",
        "snmpPrivPassphrase": "",
        "snmpPrivProtocol": "",
        "snmpUserName": "",
    }

    response = dnac.devices.add_device(**dnac_new_device_properties)

    taskId = response["response"]["taskId"]

    dnac_task = dnac.task.get_task_by_id(taskId)

    if (not dnac_task["response"]["isError"]):
        print("New device created successfully")
    else:
            print(f"Async task error seen: {dnac_task['progress']}")
