from seccomp import *
import sys



def install_filter():
    rules = SyscallFilter(defaction=KILL)
    rules.add_rule(ALLOW, "read", Arg(0, EQ, sys.stdin.fileno()))
    rules.add_rule(ALLOW, "write", Arg(0, EQ, sys.stdout.fileno()))
    rules.add_rule(ALLOW, "write", Arg(0, EQ, sys.stderr.fileno()))
    rules.add_rule(ALLOW, "fstat")
    rules.add_rule(ALLOW, 'ioctl')
    rules.add_rule(ALLOW, 'sigaltstack')
    rules.add_rule(ALLOW, "rt_sigaction")
    rules.add_rule(ALLOW, "exit_group")
    rules.add_rule(ALLOW, "read")
    rules.add_rule(ALLOW, "stat")
    rules.add_rule(ALLOW, "openat")
    rules.add_rule(ALLOW, "lseek")
    rules.add_rule(ALLOW, "close")
    rules.add_rule(ALLOW, "mmap")
    rules.add_rule(ALLOW, "brk")
    rules.add_rule(ALLOW, "getdents")
    rules.add_rule(ALLOW, "munmap")
    rules.add_rule(ALLOW, "mprotect")
    rules.add_rule(ALLOW, "access")
    rules.add_rule(ALLOW, "futex")
    rules.add_rule(ALLOW, "getrandom")
    rules.add_rule(ALLOW, "getcwd")
    rules.add_rule(ALLOW, "lstat")
    rules.add_rule(ALLOW, "fcntl")


    rules.load()


install_filter()