import subprocess, os, sys, glob

py3 = sys.version_info > (3, 0)


def pyversion():
    return [2, 3][int(py3)]


def pyinput(*args, **kwargs):
    if pyversion() == 2:
        return raw_input(*args, **kwargs)
    elif pyversion() == 3:
        return input(*args, **kwargs)
    else:
        raise NotimplementedError


def execbash(script, **kwargs):
    if py3:
        kwargs.setdefault('encoding', 'utf8')
    else:
        try:
            del kwargs['encoding']
        except KeyError:
            pass
        assert 'encoding' not in kwargs.keys()
        
    proc = subprocess.Popen("/bin/bash", 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, **kwargs)
    stdout, stderr = proc.communicate(script)
    return stdout, stderr


def whoami():
    return execbash('whoami')[0].split('\n')[0].strip()


def home():
    return execbash('echo $HOME')[0].split('\n')[0].strip()


def pwd():
    return execbash('pwd')[0].split('\n')[0].strip()


def ll(path):
    return execbash('ls -lrth %s' % path)[0]


def clearterm():
    os.system('clear')

   
def find_processes(command_search, username, currentpid, currentppid):
    script = """ps -efT | awk '$1 == "{}"' | grep '{}' | grep -v 'ps -ef' | grep -v 'grep' """.format(username , command_search)
    stdout, stderr = execbash(script, shell=True)
    h = stdout.strip().strip('\n').strip()

    pids = [int(_.split()[1]) for _ in h.split('\n')]
    ppids = [int(_.split()[2]) for _ in h.split('\n')]        
    cmds = [" ".join(_.split()[7:]) for _ in h.split('\n')]                
    for pid, ppid, cmd in zip(pids, ppids, cmds):
        if pid == currentpid:
            # this process 
            continue                
        elif ppid == currentpid:
            # parent pid is this process, ignore it
            continue
        yield pid, ppid, cmd 


def sigkill(option, command_to_kill):
    assert option.upper() in ['SIGKILL', 'SIGINT', 'SIGTERM']
    currentpid = os.getpid()
    currentppid = os.getppid()
    homepath = home()
    username = whoami()

    execcmd = []
    for pid, ppid, cmd in find_processes(
        command_to_kill, username, currentpid, currentppid):
        execcmd.append("kill -{} {}        #  {}".format(option.upper(), pid, cmd))

    execcmd = "\n".join(execcmd).strip()
    if not len(execcmd):
        print('no matching process')
        sys.exit(1)
    print(execcmd)
    if pyinput('run?') == "y":
        execbash(execcmd, shell=True)
        

def taskset(affinity, command_search):
    assert "-" in affinity
    try: 
        threadmin, threadmax = affinity.split('-')
        threadmin = int(threadmin)
        threadmax = int(threadmax)
    except Exception as e:
        e.args = ('affinity option not understood ({}), was expecting smth like 0-10'.format(affinity))
        raise e
        
    currentpid = os.getpid()
    currentppid = os.getppid()
    homepath = home()
    username = whoami()

    execcmd = []
    for pid, ppid, cmd in find_processes(
        command_search, username, currentpid, currentppid):
        execcmd.append("taskset -pc {:<7s} {:<10d} #  {}".format(affinity, pid, cmd[:80]))

    execcmd = "\n".join(execcmd).strip()
    if not len(execcmd):
        print('no matching process')
        sys.exit(1)
    print(execcmd)
    if pyinput('run?') == "y":
        execbash(execcmd, shell=True)


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

def get_device(dirname):
    return execbash('df -hT {}'.format(dirname), shell=True)[0].split('\n')[1].split()[0]
 
if __name__ == "__main__":
    print(whoami())
    print(home())
    print(pwd())
    print(ll('./*'))
