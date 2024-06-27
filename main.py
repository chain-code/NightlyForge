import argparse
import json
import os
import sys
import core
import util
import log
if __name__ == '__main__':
    #创建一个 argparse.ArgumentParser 对象，用于处理命令行参数
    parser = argparse.ArgumentParser()
    #-c 或 --components：一个可选参数，用于指定需要构建的组件项目名称，多个项目名称用逗号分隔。
    parser.add_argument('-c', '--components', help="comma seprated project names(ename) that needs to build component")
    #位置参数，指定 JSON 配置文件的路径。
    parser.add_argument('schema', help="path to json configuration file")
    #解析命令行参数，并将结果存储在 args 对象中
    args = parser.parse_args()

    schema_file = util.ReadFile(args.schema)
    if schema_file == '':
        print ('schema file not exists or empty!')
        exit(1)

    schema_dir = os.path.dirname(os.path.abspath(args.schema))
    os.chdir(schema_dir)

    sys.path.append(schema_dir)

    schema = json.loads(schema_file)
    logger = log.InitLog(log.GetLogDir(schema))

    nightly = core.Nightly(schema)
    nightly.buildInstaller()