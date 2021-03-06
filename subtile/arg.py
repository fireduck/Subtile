import os

USER_AGENT = "Subtile v0.02"
SERVICE_ADDRESS = "http://api.opensubtitles.org/xml-rpc"

OPTIONS = {"-login" : "login", "-password" : "password", "-l" : "lang", "-lang" : "lang", "-proxy" : "proxy" }

class CommandLineParser:
                        
    def __init__(self, prefs, files):
        self.prefs = prefs
        self.files = files

    def add_opt(self, opt, value):
        self.prefs[OPTIONS[opt]] = value

    def add_file(self, f):
        self.files.add(f)
        
    def parse_arg(self, arg, iterator):
        if arg in OPTIONS:            
            self.add_opt(arg, iterator.next())
        else:
            self.add_file(arg)            

    def parse(self, args):
        iterator = args.__iter__()
        for arg in iterator:
            self.parse_arg(arg, iterator)

class FileParser:

    def __init__(self, prefs):
        self.prefs = prefs

    def add_opt(self, opt, value):
        self.prefs[opt] = value
    
    def parse_line(self, line):
        opt, value = line.split('=')
        self.add_opt(opt.strip(), value.strip())

    def parse_file(self, f):
        with open(f) as fd:
            for line in fd:
                self.parse_line(line)

    def parse(self):
        f = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME'), '.subtile')
        if os.path.isfile(f):
            self.parse_file(f)

class Args:

    def __init__(self, args):     
        self.prefs = {"login" : "", "password" : ""}
        self.files = set()
        parser = CommandLineParser(self.prefs, self.files)
        parser.parse(args)
        parser = FileParser(self.prefs)
        parser.parse()

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
