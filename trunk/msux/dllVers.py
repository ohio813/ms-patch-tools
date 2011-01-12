#!/usr/bin/python
"""
dllVers.py is a simple wrapper around the pefile library that is used
to extract the file version information from a PE file.

-sean larsson, iDefense Labs, 12/30/2010
"""

import pefile
import os
import sys


#
if __name__ == "__main__":
    
    if(len(sys.argv) < 2):
        print "Usage: %s <dlls>" % sys.argv[0]
        exit(1)
        pass

    #
    try:
        pe = pefile.PE(sys.argv[1])
    except pefile.PEFormatError:
        sys.exit(1)
    
    fName = os.path.basename(sys.argv[1])
    osMajor = pe.VS_FIXEDFILEINFO.FileVersionMS >> 16
    osMinor = pe.VS_FIXEDFILEINFO.FileVersionMS & 0xffff
    swMajor = pe.VS_FIXEDFILEINFO.FileVersionLS >> 16
    swMinor = pe.VS_FIXEDFILEINFO.FileVersionLS & 0xffff
    sys.stdout.write("%d.%d.%d.%d" % (osMajor, osMinor, swMajor, swMinor))
    sys.exit(0)
