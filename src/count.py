#!/usr/bin/env python
import glob, os, sys
from subprocess import Popen, PIPE

def whoami():
    script = "whoami"
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    user = stdout.strip().strip('\n').strip()
    return user
def home_path():
    script = "cd ~; pwd"
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    h = stdout.strip().strip('\n').strip()
    return h
home = home_path()

###########################################
def countfiles(paths):
    N = 0
    NN = 0
    for d in paths:
        if not os.path.isdir(d):
            NN += 1
            continue
        cmd = 'find -L %s -type f | wc -l > ~/.countf.log' % d
        os.system(cmd)
        print d,
        with open('{}/.countf.log'.format(home), 'r') as fid:
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
        cmd = 'find -L %s -type d | wc -l > ~/.countd.log' % d
        os.system(cmd)
        print d,
        with open('{}/.countd.log'.format(home), 'r') as fid:
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
