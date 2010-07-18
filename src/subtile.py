#!/usr/bin/python


import sys
from client import Client
from arg import Args

args = Args[sys.argv[1:]]

print ("trying to connect...")
client = Client(args.get_prefs("lang"))
if client.login(args.get_prefs("login"), args.get_prefs("password")):
    print ("connected")

    client.search_sub(args.get_files())

    client.logout()
    print ("logout")

