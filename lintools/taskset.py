#!/usr/bin/env python
import sys, os
from subprocess import Popen, PIPE
from lintools.linuxcmds import taskset

help_message = """
usage :
taskset.py affinity "command keywords"
where affinity is like "0-10"
"""

        
if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print(help_message)
        sys.exit(1)
    
    taskset(affinity=sys.argv[1], command_search=sys.argv[2])
