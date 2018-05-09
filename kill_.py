#!/usr/bin/env python
import sys, os

ss = sys.argv[1:]
force = False
if "-force" in ss:
    ss.remove('-force')
    force = True

for s in ss:
   if force:
       os.system('''
       ps_.py | grep "%s" | awk '{print "echo "$2}' | grep -v 'grep' | grep -v 'kill_.py'
       ''')
   else:
       os.system("""ps_.py | grep "%s" | awk '{print "kill -SIGINT "$2" #"$0}' | grep -v 'grep' | grep -v 'kill_'""" % s)
    



