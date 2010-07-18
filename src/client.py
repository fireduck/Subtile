#!/usr/bin/python

from xmlrpclib import ServerProxy
from arg import USER_AGENT, SERVICE_ADDRESS

SUCCESS = "200 OK"

class Client:

    def __init__(self, lang):
        self.proxy = ServerProxy(SERVICE_ADDRESS, allow_none=True)
        self.lang = lang

    def login(self, login, password):
        info = self.proxy.LogIn(login, password, self.lang, USER_AGENT)
        if (info["status"] == SUCCESS):
            self.token = info["token"]
            return True
        return False

    def logout(self):
        info = self.proxy.LogOut(self.token)
        if (info["status"] == SUCCESS):
            return True
        return False

    def search_sub(self, videos):
        ask_for = []

        for video in videos:
            m = {"sublanguageid" : self.lang, "moviehash" : video.get_hash(), "moviebytesize" : video.get_size()}
            ask_for.append(m)

        info = self.proxy.SearchSubtitles(self.token, ask_for)
        print(info)


        


