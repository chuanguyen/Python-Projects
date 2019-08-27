#!/usr/bin/env python

import getpass
import telnetlib


user = input("Enter your remote account: ")
password = getpass.getpass()

file = open("myswitches")

tftp_ip = input("Enter the IP of the TFTP server: ")
print("Copying configs to the TFTP server at: {}\n".format(tftp_ip))

for line in file:
    print("Configuring current switch: {}".format(line))
    HOST = line
    # Timeout needed or the decode function fails
    tn = telnetlib.Telnet(HOST, timeout = 1)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii')+b"\n")
    if password:
         tn.read_until(b"Password: ")
         tn.write(password.encode('ascii')+b"\n")

    tn.write(b"copy run tftp:\n")
    tn.write((str(tftp_ip)+"\n").encode('ascii'))
    tn.write(b"\n")
    tn.write(b"exit\n")

file.close()
