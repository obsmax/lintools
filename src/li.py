#!/usr/bin/env python
import sys, time, os
from linuxcmds import *

searchpath = sys.argv[1]

if False:
    last = ll(searchpath)
    print last
    while True:
        current = ll(searchpath)
        if current != last:
            lines = last.split('\n')
            for line in current.split('\n'):
                if line not in lines:
                    print (line)
        last = current
        time.sleep(1.0)
else:       
    while True:    
        current = ll(searchpath)
        clearterm()
        print (current)
        time.sleep(1.0)
        
