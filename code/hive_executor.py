import subprocess
import os

def from_file(fileName: str, baseDir=os.getcwd(), subDir='.tmp'):
    r = subprocess.run('hive -f {bd}/{sd}/{fn}.sql'.format(bd=baseDir, sd=subDir, fn=fileName), shell=True)
    return r

def from_command(command: str):
    r = subprocess.run("hive -e '{hive_cmd}'".format(hive_cmd=command), shell=True)
    return r