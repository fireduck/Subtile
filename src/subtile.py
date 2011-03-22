#!/usr/bin/python

import sys
from client import Client
from arg import Args
from video import Video
from filter import IsAMovieFile, HasAsrtFile

class Launcher:

    def __init__(self, filenames):
        self.map = {}
        for filename in filenames:
            v = Video(filename)
            self.map[v.get_hash()] = v
        print(self.map)

    def run(self, args):
        print ("trying to connect...")
        client = Client(args.get_prefs("lang"))

        if client.login(args.get_prefs("login"), args.get_prefs("password")):
            print ("connected")
            client.search_sub(self.map)
            client.logout()
            print ("logout")
        else:
            print ("unable to connect with this login "+ args.get_prefs("login"))

if len(sys.argv) == 1:
    print ("subtile videos [-login <login>] [-password <password>] [-lang <lang>]")
    exit()

args = Args(sys.argv[1:])
filter = HasAsrtFile(IsAMovieFile(args.get_files()))
launcher = Launcher(filter)
launcher.run(args)





