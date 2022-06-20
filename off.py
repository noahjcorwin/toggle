#!/usr/bin/python3
import os,subprocess
cwd = os.getcwd()
black_list_file = f"{cwd}/blacklist.txt"

black_list = []
with open(black_list_file) as f:
    black_list = f.read().splitlines()

for item in black_list:
    command = ['/usr/local/bin/pihole','--regex',item,'-d']
    proc = subprocess.Popen(command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    return_code = proc.returncode
    std_out = stdout.decode("utf-8")
    std_err = stderr.decode("utf-8")
