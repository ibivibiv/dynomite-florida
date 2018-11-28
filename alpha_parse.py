import sys
import socket

alpha = ['a','b','c','d']

hostname = socket.gethostname()

tokens = hostname.split('-')

datacenter = hostname[:-2]

rackid = datacenter + alpha[int(tokens[3])]

with open('dynomite_single.yml', 'r') as myfile:
    filestring = myfile.read().replace('$DATACENTER', datacenter).replace('$RACK_ID', rackid)

file = open('dynomite_single.yml', 'w')
file.write(filestring)
file.close()
