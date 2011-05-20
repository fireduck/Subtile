#!/usr/bin/python

import sys
import os
from subtile import Client, Args

args = Args(sys.argv[1:])

client = Client(args.get_prefs("lang"), args.get_prefs("proxy"))

try:
    print ("Trying to connect...")
    if client.login("xxx", "xxx"):
        print ("Connected")
        client.logout()
        print ("Logout")
    else:
        print ("Unable to connect.")
except Exception as e:
    print ("An error has occurred: {0}".format(e))
