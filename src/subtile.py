#!/usr/bin/python

import sys
from client import Client
from arg import Args
from video import Video

class Launcher:

    def __init__(self, filenames):
        self.map = {}
        for filename in filenames:
            v = Video(filename)
            self.map[v.get_hash()] = v

    def run(self, args):
        print ("trying to connect...")
        client = Client(args.get_prefs("lang"))

        if client.login(args.get_prefs("login"), args.get_prefs("password")):
            print ("connected")
            client.search_sub(self.map)
            client.logout()
            print ("logout")

if len(sys.argv) == 1:
    print ("subtile videos [-login <login>] [-password <password>] [-lang <lang>]")
    exit()

args = Args(sys.argv[1:])
launcher = Launcher(args.get_files())
launcher.run(args)





