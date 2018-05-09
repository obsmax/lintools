#!/usr/bin/env python
import sys, os

help_message = """
usage :
kill_ -SIGTERM "some command visible in ps_"
"""

from subprocess import Popen, PIPE

def home_path():
    script = "cd ~; pwd"
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    h = stdout.strip().strip('\n').strip()
    return h
home = home_path()

if len(sys.argv) == 1:
    print help_message
    sys.exit()

ss = sys.argv[1:]
assert ss[0].startswith('-')
option = ss[0]
tmpfile = '%s/.kill_.tmp.out' % home

if os.path.exists(tmpfile):
    os.remove(tmpfile)

for s in ss:
   if s == option: continue
   os.system("""ps_ | grep "%s" | awk '{print "kill %s "$2" #"$0}' | grep -v 'grep' | grep -v 'kill_' >> %s""" % (s, option, tmpfile))


os.system('cat %s' % tmpfile)
if raw_input('run?') == "y":
    os.system("bash %s" % tmpfile)

os.system('rm -f %s' % tmpfile)
    



