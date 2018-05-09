#!/usr/bin/env python
import os, sys, glob, time
import numpy as np

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
user = whoami()


tmpfile = '%s/.ps_.tmp.txt' % home
Ncut = 160
if len(glob.glob(tmpfile)) == 1:
    os.system('trash ' + tmpfile)
elif len(glob.glob(tmpfile)) > 1:
    raise
os.system('ps -ef | grep %s > ' % user[:3] + tmpfile)
f = open(tmpfile, 'r')
L = f.readlines()
f.close()
os.system('trash ' + tmpfile)


def affiche(LLL):
    for l in LLL:
        if len(l) > Ncut:
            print l[:Ncut]
        else:
            print l.split('\n')[0]

Lpython = []
Lpy = []
Lgedit = []
Lother = []
for l in L:
    if "python " in l or "python2.7" in l:
        Lpython.append(l)
    elif ".py" in l:
        Lpy.append(l)
    elif "gedit" in l:
        Lgedit.append(l)
    else:
        Lother.append(l)
        

print "-------------------------------------------------------------"
affiche(Lother)
print "-------------------------------------------------------------"
affiche(Lgedit)
print "-------------------------------------------------------------"
affiche(Lpython)
print "-------------------------------------------------------------"
affiche(Lpy)
#            
