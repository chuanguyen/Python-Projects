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
    tn.write(user.encode('ascii')+b"\n")
    if password:
         tn.read_until(b"Password: ")
         tn.write(password.encode('ascii')+b"\n")

    tn.write(b"vlan database\n")

    for i in range(2, 9):
        # Have to encode in ASCII since write() expects bytes, not string
        # Catalyst 3600 expect VLAN configuration through VLAN database mode
        tn.write(("vlan {} name vlan{}".format(i,i)+"\n").encode('ascii'))

    tn.write(b"apply\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))
