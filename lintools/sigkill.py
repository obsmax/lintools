#!/usr/bin/env python
import sys, os
from subprocess import Popen, PIPE
from lintools.linuxcmds import sigkill

option = "SIGKILL"
help_message = """
usage :
{} "command keywords"
""".format(option.lower())

        
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print(help_message)
        sys.exit(1)
    
    sigkill(option.upper(), sys.argv[1])
