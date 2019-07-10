#!/usr/bin/env python
import sys, time, os
from linuxcmds import *


raise ValueError("obsolet, use watch 'ls -lrt | tail'")
searchpath = sys.argv[1]

while True:    
    current = ll(searchpath)
    clearterm()
    print (current)
    time.sleep(1.0)
    
