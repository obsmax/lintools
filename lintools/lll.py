#!/usr/bin/env python
from __future__ import print_function
import glob, os, sys
import numpy as np


def lll(d, level = 0, maxdepth = 1e4, directories = True, files = False):
    if maxdepth <= 0: return
    drs = np.sort(glob.glob('%s/*' % d))

    for dd in drs:
        if os.path.isdir(dd) and directories:
            if d != ".": s = "|  " * level + dd.split(d)[-1].split('/')[-1]
            else:        s = "|  " * level + dd.split('/')[-1]

            print( s + "/")
            lll(dd, level = level + 1, maxdepth = maxdepth - 1, directories = directories, files = files)
        elif files:
            if d != ".": s = "|  " * level + dd.split(d)[-1].split('/')[-1]
            else:        s = "|  " * level + dd.split('/')[-1]
            print( s)


# -------------------------------------------
if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("""
            -%d  recursion depth (default -3)
            -h   (--help) help message
            -d   do not list directories (default False)
            -f   list files (default False)
        """)
        sys.exit(1)

    # -------------------------------------------
    maxdepth = 2
    directories = True
    files = False
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            for digit in arg[1:]:
                if digit in "0123456789": maxdepth = int(digit)
                if digit == "d": directories = False
                if digit == "f": files = True


    # -------------------------------------------
    lll(".", maxdepth = maxdepth, directories = directories, files = files)
