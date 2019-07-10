#!/usr/bin/env python
from lintools.linuxcmds import whoami, execbash
import os, sys, glob, time
import numpy as np

TERMWIDTH = 160

def affiche(LLL):
    for l in LLL:
        if len(l) > TERMWIDTH:
            print(l[:TERMWIDTH])
        else:
            print(l.split('\n')[0])


if __name__ == "__main__":
    _user = whoami()
    L = execbash('ps -ef | grep {}'.format(_user), shell=True)[0].split('\n')

    # =====================
    Lpython = []
    Lpy = []
    Lgedit = []
    Lother = []
    for l in L:
        if "python " in l or "python2.7" in l:
            Lpython.append(l)
        elif ".py" in l:
            Lpy.append(l)
        elif "gedit" in l:
            Lgedit.append(l)
        else:
            Lother.append(l)
            
    # =====================
    print("-------------------------------------------------------------")
    affiche(Lother)
    print("-------------------------------------------------------------")
    affiche(Lgedit)
    print("-------------------------------------------------------------")
    affiche(Lpython)
    print("-------------------------------------------------------------")
    affiche(Lpy)
    #            

