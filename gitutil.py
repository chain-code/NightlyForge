import subprocess

import re
import pyutil
from datetime import datetime
def GetBranchName(repo_dir):
    '''获取当前分支名称'''

    cmd = 'git branch | grep ^\* | cut -d \' \' -f 2'
    name = pyutil.GetSubprocessOutput(['bash', '-c', cmd], repo_dir)

    return name.strip()

def Checkout(repo_dir, branch):
    if not branch:
        branch = 'master'

    pyutil.Execute('git checkout ' + branch, repo_dir)
    print("--切换项目{}到分支{}".format(repo_dir,branch))


def GetBranchName(repo_dir):
    '''获取当前分支名称'''

    cmd = 'git branch | grep ^\* | cut -d \' \' -f 2'
    name = pyutil.GetSubprocessOutput(['bash', '-c', cmd], repo_dir)

    return name.strip()

def Check_git_status(repo_dir):
    cmd = 'git status --porcelain'
    result = subprocess.run(['bash', '-c', cmd], cwd=repo_dir, capture_output=True, text=True)

    if result.returncode == 0:
        output = result.stdout.strip()
        return output
    else:
       return False

def Pull(repo_dir, origin='origin', branch='master'):
    if not branch:
        branch = 'master'
    pyutil.Execute('git pull --rebase ' + origin + ' ' + branch, repo_dir)


def Add(repo_dir):
    print("-- git add .")
    pyutil.Execute('git -c core.autocrlf=false add .', repo_dir)


def Commit(repo_dir):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("-- git commit -m "+current_time)
    pyutil.Execute('git -c core.autocrlf=false commit -m '+current_time, repo_dir)

def Push(repo_dir,branch='master'):
    print("-- git push origin master")
    pyutil.Execute('git push origin '+branch, repo_dir)

def GetLastCommitID(repo_dir):
    '''获取上一次提交的Hash ID'''

    cmd = 'git log|head -1|cut -d \' \' -f 2'
    hash_id = pyutil.GetSubprocessOutput(['bash', '-c', cmd], repo_dir)
    hash_id = re.sub("\W", "", hash_id)

    return hash_id
