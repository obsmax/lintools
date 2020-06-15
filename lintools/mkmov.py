#!/usr/bin/env python
from __future__ import print_function
from builtins import input
from lintools.linuxcmds import execbash
import sys, glob, os
import random, time


help_message = """
create a movie from a collection of png files
usage:
    options
        --dry-run              = prints the shell script only
        --thumbnail="filename" = name of the figure to place first for thumbnail
    arguments
        list of png files or paths to pngfiles (use quotes and wildcards)
"""

mkdir_script = '''
# ======================== BEGIN SHELL SCRIPT
trash {dirtemp}
mkdir --parents {dirtemp}'''

link_script = "\nln -sf {pngfile} {dirtemp}/_image_{i:04d}.png"
         
ffmpeg_script = '''        
ffmpeg -r {rate} -f image2 \\
    -i {dirtemp}/_image_%04d.png \\
    -vcodec libx264 \\
    -crf 25  \\
    -pix_fmt yuv420p mov.mp4
    '''
    
close_script = '''
trash {dirtemp}
# ======================== END SHELL SCRIPT
'''


if __name__ == "__main__":

    
    if os.path.isfile('mov.mp4'):
        ans = input('mov.mp4 exists, overwrite?') 
        if ans == "y":
            os.system('trash mov.mp4')
        else:
            sys.exit(1)

    # ============ defaults
    dry_run = False    
    thumbnail = None
    rate = 24 # 24   # Hz
    
    # ============ input
    ls = sys.argv[1:]
    if not len(ls):
        print(help_message)
        sys.exit(1)
    
    # ============ create the shell script
    # tmp dir
    dirtemp = "./_mkmov_{:010d}".format(int(random.random() * 1e10))
    script = mkdir_script.format(dirtemp=dirtemp)
    filename = "./mov.mp4".format(dirtemp=dirtemp)
    
    # separate options from files
    options = []
    remain = []
    for pathorfileoroption in ls:
        if pathorfileoroption.startswith('-'):
            # option
            options.append(pathorfileoroption)
        else:
            for pngfile in glob.iglob(pathorfileoroption): 
                if not pngfile.endswith('.png') or pngfile.endswith('.PNG'):
                    raise ValueError('unexpected file type {}'.format(pngfile))
                remain.append(pngfile)
    
    # check options
    for option in options:
        if option == "--dry-run":
            dry_run = True
        elif option.startswith('--thumbnail'):
            assert option.startswith('--thumbnail=')
            thumbnail = option.split('=')[-1]
            assert os.path.isfile(thumbnail)
            assert thumbnail.split('.')[-1].lower() in ['jpg', 'png']
        else:
            raise ValueError('unknown option >{}<'.format(option))
            
    i = 0  
    if thumbnail is not None:
        script += link_script.format(
            pngfile=os.path.abspath(thumbnail),  # need absolute path, not relative
            dirtemp=dirtemp,
            i=i)
        i += 1
                  
    for pngfile in remain:   
           
        script += link_script.format(
            pngfile=os.path.abspath(pngfile),  # need absolute path, not relative
            dirtemp=dirtemp,
            i=i)
        i += 1

    script += ffmpeg_script.format(rate=rate, dirtemp=dirtemp)
    script += close_script.format(dirtemp=dirtemp)
            
    # ============ print on screen
    print(script)
             
    # ============ execute shell script
    if not dry_run: 
        try:
            timeout = 60.
            start = time.time()
            stdout, stderr = execbash(script, shell=True)
            while time.time() - start <= timeout:
                if os.path.isfile(filename):
                    break             
                time.sleep(1.0)
            else:
                raise OSError('Time out, could not find {} after {}s, error : {}'.format(filename, timeout, stderr))
        except (OSError) as e:
            os.system('trash mov.mp4')            
            raise
        finally:
            if os.path.isdir(dirtemp):
                # force clean up
                script = "trash {dirtemp}".format(dirtemp=dirtemp)
                print(script)
                os.system(script)
                        
            
    
    


