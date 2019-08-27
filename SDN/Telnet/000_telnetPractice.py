import getpass
import telnetlib

HOST = "192.168.10.100"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST, timeout = 1)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
     tn.read_until(b"Password: ")
     tn.write(password.encode('ascii') + b"\n")

tn.write(b"conf t\n")
tn.write(b"do show ip int brief\n")
tn.write(b"end\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
