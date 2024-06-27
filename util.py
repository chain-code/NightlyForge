
def ReadFile(path, charset='UTF-8', binary=False):
    '''读取文件内容，返回字符串   决定是否以二进制模式读取文件'''
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