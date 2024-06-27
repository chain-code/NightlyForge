
import logging
import os

import pyutil

kLogFile = 'nightly.log'
kDebugLogFile = 'nightly_debug.log'
def GetLogDir(schema):
    ''' 获取配置文件中的log目录，若未指定使用默认值 '''
    if schema.get('location') and schema['location'].get('log'):
        #当前文件目录/log
        log_dir = os.path.join(os.path.dirname(__file__),  schema['location']['log'])

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    return log_dir

def GetLogger():
    return logging.getLogger(kLogFile)

def InitLog(log_dir):
    '''初始化日志'''
    if not os.path.exists(log_dir):
        os.mkdirs(log_dir)

    log_path = os.path.join(log_dir, kLogFile)
    if os.path.exists(log_path):
        os.remove(log_path)

    debug_log_path = os.path.join(log_dir, kDebugLogFile)
    if os.path.exists(debug_log_path):
        os.remove(debug_log_path)

    logger = logging.getLogger(kLogFile)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_hd = logging.FileHandler(log_path, encoding='utf-8')
    file_hd.setLevel(logging.INFO)
    file_hd.setFormatter(formatter)
    logger.addHandler(file_hd)

    filed_hd = logging.FileHandler(debug_log_path, encoding='utf-8')
    filed_hd.setLevel(logging.DEBUG)
    filed_hd.setFormatter(formatter)
    logger.addHandler(filed_hd)

    stream_hd = logging.StreamHandler()
    stream_hd.setLevel(logging.DEBUG)
    stream_hd.setFormatter(formatter)
    logger.addHandler(stream_hd)

    return logger
