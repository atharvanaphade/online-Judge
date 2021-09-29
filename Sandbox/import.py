import sys 
from seccomp import *


def install_filter():
    rule = SyscallFilter(defaction=KILL)
    rule.add_rule(ALLOW, "read", Arg(0, EQ, sys.stdin.fileno()))
    rule.add_rule(ALLOW, "write", Arg(0, EQ, sys.stdout.fileno()))
    rule.add_rule(ALLOW, "write", Arg(0, EQ, sys.stderr.fileno()))
    rule.add_rule(ALLOW, "fstat")
    rule.add_rule(ALLOW, 'ioctl')
    rule.add_rule(ALLOW, 'sigaltstack')
    rule.add_rule(ALLOW, "rt_sigaction")
    rule.add_rule(ALLOW, "exit_group")
    rule.add_rule(ALLOW, "read")
    rule.add_rule(ALLOW, "stat")
    rule.add_rule(ALLOW, "openat")
    rule.add_rule(ALLOW, "lseek")
    rule.add_rule(ALLOW, "close")
    rule.add_rule(ALLOW, "mmap")
    rule.add_rule(ALLOW, "brk")
    rule.add_rule(ALLOW, "getdents")
    rule.add_rule(ALLOW, "munmap")
    rule.add_rule(ALLOW, "mprotect")
    rule.add_rule(ALLOW, "access")
    rule.add_rule(ALLOW, "futex")
    rule.add_rule(ALLOW, "getrandom")
    rule.add_rule(ALLOW, "getcwd")
    
    rule.add_rule(ALLOW, "fcntl")


    rule.load()


install_filter()

#https://pkgbuild.com/~jelle/seccomp/function_reference.html