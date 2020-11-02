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

def create_dnac_devices(dnac_token):
    url = create_dnac_url("network-device/")
    headers = {"Content-Type":"application/json","x-auth-token":dnac_token}

    new_device_dict = {
        "ipAddress": ["192.0.2.1"],
        "snmpVersion": "v2",
        "snmpROCommunity": "readonly",
        "snmpRWCommunity": "readwrite",
        "snmpRetry": "1",
        "snmpTimeout":"60",
        "cliTransport": "ssh",
        "username": "calvin",
        "password": "secret123!",
        "enablePassword": "secret456!",
    }

    response = requests.post(url, headers=headers, json=new_device_dict ,verify=False)

    # Verifies the response code of the request
    if response.ok:
        # wait some time for DNA to process request
        time.sleep(10)

        # Retrieve status of request by retrieving via task ID
        taskId = response.json()["response"]["taskId"]
        task_response = requests.get(create_dnac_url(f"task/{taskId}"), headers=headers)

        if task_resopnse.ok:
            task_data = task_response.json()["response"]

            if not task_data["isError"]:
                print("New device successfully created")
            else:
                print(f"Async task reror seen: {task_data['progress']}")
        else:
                print(f"Async GET failed: status code {task_response.status_code}")
    else:
        print(f"POST response failed: {response.status_code}")

if (__name__ == "__main__"):
    dnac_token = get_token()
    dnac_devices = create_dnac_devices(dnac_token)
