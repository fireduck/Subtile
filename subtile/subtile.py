#!/usr/bin/env python

import sys
import logging
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
            logging.info("Nothing to do !")
            return

        logging.info ("Trying to connect...")
        client = Client(args.get_prefs("lang"), args.get_prefs("proxy"))

        if client.login(args.get_prefs("login"), args.get_prefs("password")):
            logging.info("Connected")
            to_download = client.search_sub(self.map)

            client.download_sub(to_download)
            client.logout()
            logging.info("Logout")
        else:
            logging.error("Unable to connect with this login "+ args.get_prefs("login"))

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    if len(sys.argv) == 1:
        print(missing_args)
        exit()

    args = Args(sys.argv[1:])

    flter = HasAsrtFile(IsAMovieFile(args.get_files()))

    try:
        launcher = Launcher(flter)
        launcher.run(args)
    except Exception as e:
        logging.error("An error has occurred: {0}".format(e))
