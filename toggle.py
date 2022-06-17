import json
import os
import subprocess
from flask import Flask
from flask_httpauth import HTTPTokenAuth

cwd = os.getcwd()

black_list_file = f"{cwd}/blacklist.txt"
token_file = f"{cwd}/tokens.txt"

with open(token_file, 'r') as f:
    tokens= json.loads(f.read())

black_list = []
with open(black_list_file) as f:
    black_list = f.read().splitlines()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/toggleon')
@auth.login_required
def toggleon():
    for item in black_list:
        command = ['pihole','--regex',item]
        proc = subprocess.Popen(command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        return_code = proc.returncode
        std_out = stdout.decode("utf-8")
        std_err = stderr.decode("utf-8")
    return 'BLOCKING ON'

@app.route('/toggleoff')
@auth.login_required
def toggleoff():
    for item in black_list:
        command = ['pihole','--regex',item,'-d']
        proc = subprocess.Popen(command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        return_code = proc.returncode
        std_out = stdout.decode("utf-8")
        std_err = stderr.decode("utf-8")
    return 'BLOCKING OFF'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# curl -H "Authorization: Bearer xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -X GET http://127.0.0.1:5000
