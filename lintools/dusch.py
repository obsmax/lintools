#!/usr/bin/env python
from lintools.linuxcmds import execbash
import subprocess
import sys
import numpy as np

"""
same as du -sch but ordered by size
"""

#p = subprocess.Popen('du -sc ' + " ".join(sys.argv[1:]),
    #shell = True, stdout = subprocess.PIPE)
#stdout, _ = p.communicate()
#stdout = str(stdout)

stdout = execbash('du -sc ' + " ".join(sys.argv[1:]), shell=True)[0]
s, d = zip(*[(int(_.split('\t')[0]), _.split('\t')[1]) for _ in stdout.split('\n') if _.strip() != ''])
I = np.argsort(s)

cmd = 'du -sch ' + " ".join([d[i] for i in I if "total" not in d[i]])
subprocess.call(cmd, shell = True)#, stdout = subprocess.PIPE)
#execbash(cmd, shell = True)#, stdout = subprocess.PIPE)
