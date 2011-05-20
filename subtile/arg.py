USER_AGENT = "Subtile v0.01"
SERVICE_ADDRESS = "http://api.opensubtitles.org/xml-rpc"

OPTIONS = {"-login" : "login", "-password" : "password", "-l" : "lang", "-lang" : "lang", "-proxy" : "proxy" }

class Args:

    def __init__(self, args):     
        self.prefs = {"login" : "", "password" : ""}
        self.files = set()
        self.parse_args(args)
        
    def parse_args(self, args):
        iterator = args.__iter__()
        for arg in iterator:
            self.parse_arg(arg, iterator)

    def parse_arg(self, arg, iterator):
        if arg in OPTIONS:
            self.prefs[OPTIONS[arg]] = iterator.next()
        else:
            self.files.add(arg)

    def get_prefs(self, name):
        if name in self.prefs:
            return self.prefs[name]
        else:
            return None

    def get_files(self):
        return self.files


missing_args = """subtile videos_files [-login <login>] [-password <password>] [-lang <lang>] [-proxy <address:port>]
Powered by www.OpenSubtitles.org
"""

if __name__ == "__main__":

    example1 = Args(["-login", "LOGIN", "OTHER"])
    if example1.get_prefs("login") == 'LOGIN':
        print ("OK")
    else:
        print ("FAIL")
    print example1.get_files()
