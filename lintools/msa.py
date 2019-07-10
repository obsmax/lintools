#!/usr/bin/env python

"""
monitor script activity every 1s
if a script is found in ps -ef
I print the corresponding pstree -Aap 
"""


import os, sys

cmd = """
while true; 
    do sleep 1
    pid=`ps -ef | grep "%s" | grep -v grep | grep -v "%s" | awk '{print $3}' | head -n 1`

    if [ -z $pid ];
        then
        clear
        echo "%s : no activity found"
    else
        pstree -Aap $pid > ~/.monitor_script_activity.out
        clear
        cat ~/.monitor_script_activity.out
    fi 
done
""" % (sys.argv[1], 
       __file__.split('/')[-1], 
       sys.argv[1])

os.system(cmd)
