import os

def run_command(cmd):
    output = tmp = os.popen(cmd).read()
    return output