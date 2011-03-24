from xmlrpclib import ServerProxy
import base64, os
import StringIO, gzip, zlib
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
        print (info["status"])
        return False

    def logout(self):
        info = self.proxy.LogOut(self.token)
        if (info["status"] == SUCCESS):
            return True
        return False

    def search_sub(self, videos):
        ask_for = []

        for hash, video in videos.items():
            m = {"sublanguageid" : self.lang, "moviehash" : hash, "moviebytesize" : video.get_size()}
            ask_for.append(m)

        info = self.proxy.SearchSubtitles(self.token, ask_for)

        if info.has_key("data"):
            for sub in info["data"]:
                self._select_subs(videos, sub)
        
        to_download = {}
        for v in videos.values():
            to_download[v.get_sub_id()] = v
            print (v.name + " - " + v.get_sub_id())
    
        return to_download

    def _select_subs(self, videos, sub):
        video = videos[sub["MovieHash"]]
        if not video.get_sub_id():
            video.sub_id = sub["IDSubtitleFile"]


    def download_sub(self, to_download):
        if len(to_download) == 0:
            return 0

        answer = self.proxy.DownloadSubtitles(self.token, to_download.keys())
        
        if answer.has_key("data"):
            if answer['data'] == False:
                return False
            for sub in answer['data']:
                self.base_to_file(sub['data'], to_download[sub['idsubtitlefile']])
            return answer['data']
        
    def base_to_file(self, base_data, video):
        compressedstream = base64.decodestring(base_data)
        gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(compressedstream))
        s=gzipper.read()
        gzipper.close()
        subtitle_file = file(video.get_sub_filename(),'wb')
        subtitle_file.write(s)
        subtitle_file.close()

