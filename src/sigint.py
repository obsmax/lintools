#!/usr/bin/env python
import sys, os
from subprocess import Popen, PIPE

help_message = """
usage :
sigint "some command visible in ps_"
"""

option = "SIGINT"


def get_home_path():
    script = "cd ~; pwd"
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    h = stdout.strip().strip('\n').strip()
    return h
    
def get_user_name():
    script = "whoami"
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    h = stdout.strip().strip('\n').strip()
    return h
        
    
def find_processes(command_search, username, currentpid, currentppid):
    script = """ ps -ef | awk '$1 == "%s"' | grep '%s' | grep -v 'ps -ef' | grep -v 'grep' """  \
        % (username , command_search)
    p = Popen(script, stdout=PIPE, shell = True)#, stderr = stderrfid)
    stdout, stderr = p.communicate()
    h = stdout.strip().strip('\n').strip()

    # print h

    pids = [int(_.split()[1]) for _ in h.split('\n')]
    ppids = [int(_.split()[2]) for _ in h.split('\n')]    
    cmds = [" ".join(_.split()[7:]) for _ in h.split('\n')]            
    for pid, ppid, cmd in zip(pids, ppids, cmds):
        if pid == currentpid:
            # this process 
            continue            
        elif ppid == currentpid:
            # parent pid is this process, ignore it
            continue
        yield pid, ppid, cmd

        
if __name__ == "__main__":
    currentpid = os.getpid()
    currentppid = os.getppid()        
    homepath = get_home_path()
    username = get_user_name()
    # print username, homepath, currentpid, currentppid

    execcmd = []
    for pid, ppid, cmd in find_processes(sys.argv[1], username, currentpid, currentppid):
        execcmd.append("kill -{} {}        #  {}".format(option.upper(), pid, cmd))

    print "\n".join(execcmd)
    if input('run?') == "y":
        os.system(execcmd)




