#!/usr/bin/python2.7
import os, sys, time
import subprocess

if not os.path.exists('/usr/bin/iostat'):
    raise Exception('iostat is not installed')

hlp = """
monitor disk activity (read and write)
neads iostat from sysstat (sudo apt install sysstat)
please enter any directory that is inside the partition to monitor
--help : print this message and exit
--plot : make a graphic
"""
plot = False
if len(sys.argv) == 1 or "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
    print hlp
    sys.exit()

if "--plot" in sys.argv[1:] or "-p"  in sys.argv[1:]:
    plot = True
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize = (16, 3))
    fig.subplots_adjust(bottom = 0.3, left = 0.1, right = 0.95)
    ax  = fig.gca()
    fig.show()


# ----------------------------
directory = ""
for arg in sys.argv[1:]:
    if arg[0] == "-" : continue
    directory = arg
    break


# ----------------------------
device = subprocess.Popen("df -hT %s" % directory, stdout = subprocess.PIPE, shell = True).communicate()[0].split('\n')[1].split()[0]
print '>> directory "%s" is on device "%s"' % (os.path.realpath(directory), device)


# ----------------------------
Nbar = 30
scale = 200.
cmd = "/usr/bin/iostat %s" % (device)
refresh = 2.0 #not too low, may slow ios down
print cmd
T, KR, KW = None, None, None
while True:
    l = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True).communicate()[0].split('\n')
    t  = time.time()
    tt = time.asctime().split()[3]
    while len(l):
        ll = l.pop(0)
        if not len(ll): continue
        if ll.split()[0] == "Device:": break
    l = l.pop(0)
    kr = float(l.split()[4])
    kw = float(l.split()[5])
    if T is not None: 
        rspeed = round((kr - KR) / (t - T))
        wspeed = round((kw - KW) / (t - T))
        rbars = int(rspeed / scale)
        wbars = int(wspeed / scale)
        if rbars > Nbar or wbars > Nbar:
            scale *= 2
            rbars = int(rspeed / scale)
            wbars = int(wspeed / scale)
        if (rspeed or wspeed) and (rbars == 0 and wbars == 0):
            scale /= 2
            rbars = int(rspeed / scale)
            wbars = int(wspeed / scale)
        rbars = min([rbars, Nbar])
        wbars = min([wbars, Nbar])
        rbars = ("|" * rbars + " " * (Nbar - rbars))# + " " * (30 - rbars))
        wbars = ("|" * wbars + " " * (Nbar - wbars))# + " " * (30 - rbars))

        #print "%s %s read %8.0f kB/s write %8.0f kB/s" % (device, tt, round((kr - KR) / (t - T)), round((kw - KW) / (t - T)))
        L = "%s %s r[%s %8.0fkB/s]    w[%s %8.0fkB/s]  x%.0f" % (device, tt, rbars, rspeed, wbars, wspeed, scale)

        sys.stdout.write(L + "\n")
        sys.stdout.flush()

        #---------------
        if plot:
            try:
                ax.plot([t, lastt], [rspeed, lastrspeed], 'ko-')
                ax.plot([t, lastt], [wspeed, lastwspeed], 'ro-')
                xticks = ax.get_xticks()
                ax.set_xticklabels([time.ctime(w).split()[3] for w in xticks], rotation = -30, horizontalalignment = "left", verticalalignment = "top")
            except KeyboardInterrupt: raise
            except:
                ax.plot(t, rspeed, 'ko-', label="read")
                ax.plot(t, wspeed, 'ro-', label="write")
                ax.grid(True)
                ax.set_ylabel('ios (kB/s)')
                ax.set_xlabel('time')
                ax.set_title(device)
                plt.legend()
            ax.figure.canvas.draw()
            lastt, lastrspeed, lastwspeed = t, rspeed, wspeed
        #---------------

    T, KR, KW = t, kr, kw
    time.sleep(refresh)
