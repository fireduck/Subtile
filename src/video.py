#!/usr/bin/python

import struct
import os
import sys

LONGLONG_FORMAT = "q"
_64K = 65536
BYTE_SIZE = struct.calcsize(LONGLONG_FORMAT)

class Video:

    def __init__(self, name):
        self.name = name
        self.size = os.path.getsize(self.name)

        if self.size < _64K * 2:
            return "SizeError"
        self.sub_id = None
        self.hash = None
        self._calculate_hash()

    def _calculate_hash(self):
        hash = self.size
        
        with open(self.name, "rb") as f:
            hash = self._calculate_64k_hash(f, hash)
            f.seek(-_64K, os.SEEK_END)
            hash = self._calculate_64k_hash(f, hash)

        self.hash = "%016x" % hash

    def _calculate_64k_hash(self, f, hash):
        for x in range(_64K / BYTE_SIZE):
            buffer = f.read(BYTE_SIZE)
            (l_value,) = struct.unpack(LONGLONG_FORMAT, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
        return hash

    def get_hash(self):
        return self.hash
    
    def get_size(self):
        return self.size

    def get_sub_id(self):
        return self.sub_id

    def get_sub_filename(self):
        basename, extension = os.path.splitext(self.name)
        return basename + ".srt"


if __name__ == "__main__":

    print ("\nShould be:")
    print ("breakdance : 8e245d9679d31e12")
    print ("dummy.rar : 2a527d74d45f5b1b\n")

    for x in sys.argv[1:]:
        file = Video(x)
        print (file.name + " : " +file.get_hash())
