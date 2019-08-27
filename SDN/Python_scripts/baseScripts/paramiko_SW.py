#!/usr/bin/env python

import paramiko
import time

ip_address = "192.168.10.100"
username = "admin"
password = "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address,username=username,password=password)

print("Successful connection", ip_address)

remote_connection = ssh_client.invoke_shell()

remote_connection.send("configure terminal\n")
remote_connection.send("int loop 0\n")
remote_connection.send("ip address 1.1.1.1 255.255.255.255\n")
remote_connection.send("int loop 1\n")
remote_connection.send("ip address 2.2.2.2 255.255.255.255\n")

remote_connection.send("end\n")

time.sleep(1)
output = remote_connection.recv(65535)
print(output)

ssh_client.close
