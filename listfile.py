import os
def list_md_files(rootdir):
    _files = []

    #列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)
    
    for i in range(0,len(list_file)):

        # 构造路径
        path = os.path.join(rootdir,list_file[i])

        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归
        
        if os.path.isdir(path):
            _files.extend(list_md_files(path))
        if os.path.isfile(path):
            if(path.endswith('.md')):
                _files.append(path)
    return _files
