#!/usr/bin/env python

"""
obselet
find the pid of the group leader 
use 
to set nice to low priority :
renice -n 10  -g PID
"""

#import sys, os, signal, numpy as np

#from subprocess import Popen, PIPE
#def whoami():
    #script = "whoami"
    #p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    #stdout, stderr = p.communicate()
    #stdout = str(stdout)
    #stderr = str(stderr)
    #user = stdout.strip().strip('\n').strip()
    #return user
#def home_path():
    #script = "cd ~; pwd"
    #p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    #stdout, stderr = p.communicate()
    #stdout = str(stdout)
    #stderr = str(stderr)    
    #h = stdout.strip().strip('\n').strip()
    #return h
#home = home_path()
#username = whoami()


#if len(sys.argv) < 3: 
    #print 'usage : renice_ 0-10 "command indications"'
    #print 'see also, ps_, kill_, renice_'
    #sys.exit()
    
#renicecommand = " -n " + str(sys.argv[1])
#command        = " ".join(sys.argv[2:]) #part of the command line refering to a process to run renice on

#cmd = """ps -ef | awk '$1 == "%s" || $1 == "maximil+" {print substr($0, 0, 150)}' | grep "%s" | grep -v "grep"  | grep -v "renice" > %s/.renice.out.tmp""" % (username, command, home)
#print cmd
#os.system(cmd)

#with open('%s/.renice.out.tmp' % home, 'r') as fid:
    #ls, pids, ppids = [], [], []
    #for l in fid.readlines():
        #l = l.split('\n')[0]
        #pid  = l.split()[1].strip()
        #ppid = l.split()[2].strip()
        #ls.append(l)
        #pids.append(pid)  
        #ppids.append(ppid)  
    #ls, pids, ppids = [np.array(x) for x in ls, pids, ppids]

#---------------------------------------------------
#if not len(ls):
    #print "no matching process"
    #exit()
#---------------------------------------------------
#cmd = "" 

#for  i in xrange(len(ls)):
    #cmd += "renice %s %s         #%s\n" % (renicecommand, pids[i], " ".join(ls[i].split()[7:]))



#print
#print cmd
#if raw_input('do run the command? y/[n]') == "y":
    #os.system(cmd)
