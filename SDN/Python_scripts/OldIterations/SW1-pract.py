#!/usr/bin/env python

import getpass
import telnetlib


user = input("Enter your remote account: ")
password = getpass.getpass()

for n in range (100, 105):
    HOST = "192.168.10."+str(n)
    # Timeout needed or the decode function fails
    tn = telnetlib.Telnet(HOST, timeout = 1)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
         tn.read_until(b"Password: ")
         tn.write(password.encode('ascii') + b"\n")

    tn.write(b"conf t\n")

    # for i in range(1, 9):
    #     # Have to encode in ASCII since write() expects bytes, not string
    #     tn.write(("vlan "+str(i)+"\n").encode('ascii'))
    #     tn.write(("name vlan"+str(i)+"\n").encode('ascii'))
    #
    # tn.write(b"exit\n")
    # tn.write(b"do show ip int brief\n")
    tn.write(b"do wr mem\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))
