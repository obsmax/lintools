#!/usr/bin/env python
import sys, os

help_message = """
usage :
kill_ -SIGTERM "some command visible in ps_"
"""

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

if len(sys.argv) == 1:
    print help_message
    sys.exit()

ss = sys.argv[1:]
assert ss[0].startswith('-')
option = ss[0]

if os.path.exists('%s/.kill_.tmp.out' % home):
    os.remove('%s/.kill_.tmp.out' % home)

for s in ss:
   if s == option: continue
   os.system("""ps_ | grep "%s" | awk '{print "kill %s "$2" #"$0}' | grep -v 'grep' | grep -v 'kill_' >> %s/.kill_.tmp.out""" % (s, option, home))


os.system('cat %s/.kill_.tmp.out' % home)
if raw_input('run?') == "y":
    os.system("bash %s/.kill_.tmp.out" % home)

os.system('rm -f %s/.kill_.tmp.out' % home)
    



