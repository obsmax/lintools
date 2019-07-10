#!/usr/bin/env python
from __future__ import print_function
from lintools.linuxcmds import execbash, rglob
import glob, os, sys
import subprocess
import numpy as np


if __name__ == "__main__":

    if not len(sys.argv) > 1:
        print('''sum the total disk usage for each file format found in a directory (and sub directories)
usage: 
    sizbytyp dirname''')
        sys.exit(1)

    dirname = sys.argv[1]

    extensions = []
    for item in rglob(dirname):
        if os.path.isfile(item):
            extension = item.split('/')[-1]
            if "." in extension:
                extension = extension.split('.')[-1]
            else:
                continue
            if not extension in extensions:
                extensions.append(extension)
    print (extensions)
    sizes = []
    isizes = []
    for extension in extensions:
        cmd = "find {} -type f -name '*.{}' -print0 | xargs -0 du -ch | grep total | awk '{{print $1}}'".format(dirname, extension)
        #print(cmd)
        out, err = execbash(cmd)
        #print(out)
        sz = out.split()[0]
        sizes.append(sz)
        isz = eval(sz.replace('B','').replace('K', '*1e3').replace('M', '*1e6').replace('G', '*1e9').replace(',', '.'))
        isizes.append(isz)

    I = np.argsort(isizes)
    sizes = [sizes[i] for i in I]
    extensions = [extensions[i] for i in I]

    for ext, sz in zip(extensions, sizes):
        print ('*.{:<20s} {}'.format(ext, sz))

