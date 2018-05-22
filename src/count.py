#!/usr/bin/env python
import glob, os, sys


###########################################
def countfiles(paths):
    N = 0
    NN = 0
    for d in paths:
        if not os.path.isdir(d):
            NN += 1
            continue
        cmd = 'find -L %s -type f | wc -l > /tmp/countf.log' % d
        os.system(cmd)
        print d,
        with open('/tmp/countf.log', 'r') as fid:
            n = int(fid.readline().split('\n')[0])
            print n
            N += n
    print "single files", NN
    N += NN
    print "Total %d files found" % N
    return N


###########################################
def countdirs(paths):
    N = 0
    for d in paths:
        if not os.path.isdir(d): continue
        cmd = 'find -L %s -type d | wc -l > /tmp/countd.log' % d
        os.system(cmd)
        print d,
        with open('/tmp/countd.log', 'r') as fid:
            n = int(fid.readline().split('\n')[0])
            print n
            N += n
    print "Total %d directories found" % N
    return N


###########################################
if __name__ == "__main__":
    mode = None
    paths = []
    for path in sys.argv[1:]:
        if path[0] == "-":
            mode = path[1:]
        else:
            paths.append(path)
    if mode is None: mode = "f"
    ###########################################
    if "f" in mode:
        countfiles(paths)
    if "d" in mode:
        countdirs(paths)

    # countfiles(sys.argv[1:])
    #
