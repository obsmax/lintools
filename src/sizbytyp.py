#!/usr/bin/env python
from __future__ import print_function
import glob, os, sys
import subprocess
import numpy as np

def execbash(script):
    proc = subprocess.Popen("/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(script)
    return out, err

def rglob(dirname):
    """list files recursively with absolute path
    """
    if     '*' in dirname \
        or '?' in dirname \
        or '[' in dirname \
        or ']' in dirname \
        or '{' in dirname \
        or '}' in dirname : raise Exception('')

    if os.path.isfile(dirname) or os.path.islink(dirname):
        yield os.path.abspath(dirname)
        raise StopIteration('')

    for item in glob.iglob(dirname + '/*'):
        if os.path.isdir(item):
            for iitem in rglob(item):
                yield os.path.abspath(iitem)
        else:
            yield item

#-----------------------

extensions = []
for item in rglob(sys.argv[1]):
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
    cmd = "find . -type f -name '*.{}' -print0 | xargs -0 du -ch | grep total | awk '{{print $1}}'".format(extension)
    out, err = execbash(cmd)
    sz = out.split()[0]
    sizes.append(sz)
    isz = eval(sz.replace('B','').replace('K', '*1e3').replace('M', '*1e6').replace('G', '*1e9').replace(',', '.'))
    isizes.append(isz)

I = np.argsort(isizes)
sizes = [sizes[i] for i in I]
extensions = [extensions[i] for i in I]

for ext, sz in zip(extensions, sizes):

    print ('*.{:<20s} {}'.format(ext, sz))




