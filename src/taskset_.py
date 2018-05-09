#!/usr/bin/env python
import sys, os, signal, numpy as np

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
username = whoami()


if len(sys.argv) <= 1 or not sys.argv[1] == "-pc": 
    print 'usage : taskset_ -pc 0-10 "command indications"'
    print 'see also, ps_, kill_, renice_'
    sys.exit()
tasksetcommand = " ".join(sys.argv[1:-1])
processes      = sys.argv[2]
command        = " ".join(sys.argv[3:]) #part of the command line refering to a process to run taskset on



cmd = """ps -ef | awk '$1 == "%s" || $1 == "maximil+" {print substr($0, 0, 150)}' | grep "%s" | grep -v "grep"  | grep -v "taskset" > %s/.taskset.out.tmp""" % (home, command, username)
print cmd
os.system(cmd)

with open('%s/.taskset.out.tmp' % home) as fid:
    ls, pids, ppids = [], [], []
    for l in fid.readlines():
        l = l.split('\n')[0]
        pid  = l.split()[1].strip()
        ppid = l.split()[2].strip()
        ls.append(l)
        pids.append(pid)  
        ppids.append(ppid)  
    ls, pids, ppids = [np.array(x) for x in ls, pids, ppids]

#---------------------------------------------------
if not len(ls):
    print "no matching process"
    exit()
#---------------------------------------------------
cmd = "" 

for  i in xrange(len(ls)):
    cmd += "taskset %s %s         #%s\n" % (tasksetcommand, pids[i], " ".join(ls[i].split()[7:]))



print
print cmd
if raw_input('do run the command? y/[n]') == "y":
    os.system(cmd)
