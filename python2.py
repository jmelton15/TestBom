import subprocess
import os
import configparser


cmd = f'cdxgen --server'
cmd_result = subprocess.call(cmd,shell=True)