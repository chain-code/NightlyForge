import queue


import pyutil
import os
import json
import gitutil
import log
logger = log.GetLogger()
kLastBuildFile = 'LastVersion.txt'

class Nightly:
    def __init__(self, schema):
        self.schema = schema
        self.observers = {}


    def buildInstaller(self):
        logger.debug('开始每日更新文档')
        print("开始上传")
        print("开始读取上次构建的信息")
        self.LoadLastBuildInfo()
        print("开始切换项目分支")
        self.CheckoutProjects()
        print("开始拉取代码")
        self.UpdateProjects()
        print("开始生成Hugo")
        self.UpdateHugo()
        print("代码提交")
        self.PushProjects()
        print("发送邮件")
        # 发送邮件

       # if self.GetOption('send_mail', True):
            # comment_issue = self.GetOption('comment_issue', False)
            # mailer.SendMail(self.schema, last_build, version, download_links, comment_issue)
       # if self.GetOption('record_version', True):
            #self.RecordBuildVersion(version)

    def PushProjects(self):
        for project in self.schema['projects']:
            if os.path.exists(project['path']) and gitutil.Check_git_status(project['path']):
                gitutil.Add(project['path'])
                gitutil.Commit(project['path'])
                gitutil.Push(project['path'],project['branch'])


    def UpdateHugo(self):
        if self.GetOption('hugo', False):
            logger.info('正在生成hugo文件')
            print("--正在生成hugo文件")
            pyutil.Execute('hugo',"../")
    def LoadLastBuildInfo(self):
        ''' 获取上次构建的信息，并初始化 last_build '''
        global last_build
        log_dir = log.GetLogDir(self.schema)

        prev_ver = pyutil.ReadFile(os.path.join(log_dir, kLastBuildFile))
        if prev_ver:
            last_build = json.loads(prev_ver)


    def CheckoutProjects(self):
        for project in self.schema['projects']:
            if os.path.exists(project['path']):
                branch = self.GetProjectOption(project, 'branch', gitutil.GetBranchName(project['path']))
                gitutil.Checkout(project['path'], branch, submodule=project.get('sync_submodule'))

    def GetProjectOption(self, project, key, default):
        ''' 获取项目选项，如果项目没有指定该选项尝试获取全局选项，如果没有全局选项则使用默认值 '''
        if not 'options' in project or not key in project['options']:
            return self.GetOption(key, default)

        return project['options'][key]

    def GetOption(self, key, default):
        ''' 获取全局选项 '''
        if not 'options' in self.schema or not key in self.schema['options']:
            logger.debug('选项 ' + key + ' 没有被设置，使用默认值 ' + str(default))
            return default

        return self.schema['options'][key]
    def UpdateProjects(self):
        ''' 同步所有项目的代码 '''
        tasks = queue.Queue()
        concurrency = self.GetOption('concurrency', 1)
        for project in self.schema['projects']:
            if project['pull']:
                tasks.put(project)

        self.hasNewCommit=False
        pyutil.RunParallel(self.UpdateProject, tasks, concurrency)

        if not self.hasNewCommit :
            logger.info('没有拉到任何东西')
            #有没有拉取到代码好像没什么用，如果没拉到，并不代表本地没有修改 也需要提交
            #exit(1)

    def UpdateProject(self, project):

        branch = project['branch'] if project.get('branch') else gitutil.GetBranchName(project['path'])

        logger.info('正在同步' + project['ename'] + ' (' + branch + ')')
        print("--正在同步{}代码".format(project['ename']))
        gitutil.Pull(project['path'],  branch=branch)
        prev_commit = last_build.get(project['ename'])
        new_commit = gitutil.GetLastCommitID(project['path'])
        if new_commit != prev_commit:
            self.hasNewCommit=True