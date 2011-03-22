import os.path

class Filter:

    def __init__(self, iterable):
        self.iterable = iterable.__iter__()

    def __iter__(self):
        return self

    def next(self):
        i = self.iterable.next()
        if i != None and self.filtered(i):
            return self.next()
        return i
    
    def filtered(self, i):
        return False


MOVIE = [".avi", ".mkv", ".mp4"]

class IsAMovieFile(Filter):

    def filtered(self, i):
        if not os.path.isfile(i):
            print  (i + " is not a file.")
            return True
        for m in MOVIE:
            if i.endswith(m):
                return False
        print (i + " is not a movie file.")
        return True

class HasAsrtFile(Filter):
    
    def filtered(self, i):
        for m in MOVIE:
            if i.endswith(m):
                srt = i.replace(m, ".srt")
                if (os.path.isfile(srt)):
                    print (i + " has already a srt file")
                    return True
                return False
        return True
            
                



    

