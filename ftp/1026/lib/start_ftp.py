# -*- coding:UTF-8 -*

import optparse
from MyFtpServer import *
import errno
import os
import sys
import atexit
import signal

WORKDIR = os.getcwd()
PID_FILE = "/opt/pyftpdlib.pid"
LOG_FILE = "/opt/pyftpdlib.log"


def start():
    ftp = MyFtpServer()
    if util.is_linux():
        # pid = get_pid()
        # if pid and pid_exists(pid):
        #    sys.exit('daemon already running (pid %s)' % pid)
        w_pid()
    ftp.start()


def stop():
    # ps -ef|grep ftp
    # kill -9 4914
    pid = get_pid()
    print pid
    if not pid or not pid_exists(pid):
        sys.exit("daemon not running")

    sig = signal.SIGTERM
    i = 0
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            os.kill(pid, sig)
        except OSError as err:
            if err.errno == errno.ESRCH:
                print("\nstopped (pid %s)" % pid)
                return
            else:
                raise
        i += 1
        if i == 25:
            sig = signal.SIGKILL
        elif i == 50:
            sys.exit("\ncould not kill daemon (pid %s)" % pid)
        time.sleep(0.1)


def status():
    pid = get_pid()
    if not pid or not pid_exists(pid):
        print("daemon not running")
    else:
        print("daemon running with pid %s" % pid)
    sys.exit(0)


def w_pid():
    pid = os.fork()
    if pid > 0:
        # exit first parent
        sys.exit(0)

    # decouple from parent environment
    os.chdir(WORKDIR)
    os.setsid()
    os.umask(0)

    # do second fork
    pid = os.fork()
    if pid > 0:
        # exit from second parent
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()
    si = open(LOG_FILE, 'r')
    so = open(LOG_FILE, 'a+')
    se = open(LOG_FILE, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    # write pidfile
    pid = str(os.getpid())
    with open(PID_FILE, 'w') as f:
        f.write("%s\n" % pid)
    atexit.register(lambda: os.remove(PID_FILE))


def get_pid():
    """Return the PID saved in the pid file if possible, else None."""
    try:
        with open(PID_FILE) as f:
            return int(f.read().strip())
    except IOError as err:
        if err.errno != errno.ENOENT:
            raise


def pid_exists(pid):
    """Return True if a process with the given PID is currently running."""
    try:
        os.kill(pid, 0)
    except OSError as err:
        return err.errno == errno.EPERM
    else:
        return True


def main():
    global PID_FILE, LOG_FILE
    USAGE = "python [-p PIDFILE] [-l LOGFILE]\n\n" \
            "Commands:\n  - start\n  - stop\n  - status"
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-l', '--logfile', dest='logfile',
                      help='the log file location')
    parser.add_option('-p', '--pidfile', dest='pidfile', default=PID_FILE,
                      help='file to store/retreive daemon pid')
    options, args = parser.parse_args()

    if options.pidfile:
        PID_FILE = options.pidfile
    if options.logfile:
        LOG_FILE = options.logfile

    print args
    if not args:
        start()
    else:
        if len(args) != 1:
            sys.exit('too many commands')
        elif args[0] == 'start':
            start()
        elif args[0] == 'stop':
            stop()
        elif args[0] == 'restart':
            try:
                stop()
            finally:
                start()
        elif args[0] == 'status':
            status()
        else:
            sys.exit('invalid command')


if __name__ == '__main__':
    sys.exit(main())
