import subprocess, os

def execbash(script):
    proc = subprocess.Popen("/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(script)
    return out, err

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
    
if __name__ == "__main__":
    print whoami()
    print home()
    print pwd()
    print ll('./*')
