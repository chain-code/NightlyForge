import os
import tempfile
import subprocess
import traceback

import threading
import log
logger = log.GetLogger()

def GetSubprocessOutput(args, cwd=None):
    ''' 创建子进程并获取其标准输出，子进程结束后才返回 '''
    tf = tempfile.TemporaryFile()
    child = subprocess.Popen(args, stdout=tf, cwd=cwd)
    child.wait()

    tf.seek(0)
    output = tf.read().decode()
    tf.close()

    return output

def Execute(cmd, cwd=None):
    '''执行命令并获取返回值'''
    child = subprocess.Popen(cmd, shell=True, cwd=cwd)
    child.wait()

    return child.returncode

def ReadFile(path, charset='UTF-8', binary=False):
    '''读取文件内容，返回字符串'''
    try:
        if binary:
            f = open(path, 'rb')
        else:
            f = open(path, 'r', encoding=charset)
        content = f.read()
        f.close()
        return content
    except IOError:
        return ''

def movetree(src, dst):
    '''将src目录重命名为dst，会处理只读文件的情况'''
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        os.chmod(s, 0o755)
        if os.path.isdir(s):
            movetree(s, d)
        else:
            os.rename(s, d)

    os.chmod(src, 0o755)
    os.rmdir(src)

def RunParallel(work_func, queue, num_threads):

    def ThreadMain(task):
        while True:
            item = queue.get()
            if item is None:
                break
            try:
                work_func(item)
            except:
                logger.error(traceback.format_exc())
                os._exit(1)

            queue.task_done()

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=ThreadMain, args=(queue,))
        t.start()
        threads.append(t)

    # block until all tasks are done
    queue.join()

    # stop workers and cleanup
    for i in range(num_threads):
        queue.put(None)
    for t in threads:
        t.join()