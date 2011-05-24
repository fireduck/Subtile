#!/usr/bin/env python

import sys
from client import Client
from arg import Args, missing_args
from video import Video
from filter import IsAMovieFile, HasAsrtFile

class Launcher:

    def __init__(self, filenames):
        self.map = {}
        for filename in filenames:
            v = Video(filename)
            self.map[v.get_hash()] = v

    def run(self, args):

        if len(self.map) == 0:
            print ("Nothing to do !")
            return

        print ("Trying to connect...")
        client = Client(args.get_prefs("lang"), args.get_prefs("proxy"))

        if client.login(args.get_prefs("login"), args.get_prefs("password")):
            print ("Connected")
            to_download = client.search_sub(self.map)

            client.download_sub(to_download)
            client.logout()
            print ("Logout")
        else:
            print ("Unable to connect with this login "+ args.get_prefs("login"))

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print (missing_args)
        exit()

    args = Args(sys.argv[1:])

    flter = HasAsrtFile(IsAMovieFile(args.get_files()))

    try:
        launcher = Launcher(flter)
        launcher.run(args)
    except Exception as e:
        print ("An error has occurred: {0}".format(e))
