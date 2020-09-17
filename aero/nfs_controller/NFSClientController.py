# Author: Ragy Haddad
import sys,os 
import shlex
from subprocess import Popen,PIPE

# Utility Functions for Controlling NFSControllerAPI

# LS CMD
def ls_cmd(path):
    output = ""
    cmd_args = ["ls","-lhr",path]
    cmd = Popen(cmd_args,stdout=PIPE,stderr=PIPE,shell=False)
    for line in cmd.stdout:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    for line in cmd.stderr:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    return output

# MKDIR CMD
def mkdir_cmd(path):
    output = ""
    cmd_args = ["mkdir",path] 
    cmd = Popen(cmd_args,stdout=PIPE,stderr=PIPE,shell=False)
    for line in cmd.stdout:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    for line in cmd.stderr:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    return output

# Execute Commands on NFS Client
# @TODO: Handle Proper Execution
def exec_cmd(cmd):
    output = ""
    cmd_args = shlex.split(cmd) # Parse String To Correct ARGS
    print(cmd_args)
    cmd = Popen(cmd_args,stdout=PIPE,stderr=PIPE,shell=False)
    for line in cmd.stdout:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    for line in cmd.stderr:
        output += line.decode("utf-8").rstrip()
        output += "\n"
    return output




    