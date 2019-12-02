import os
from listfile import list_md_file

# 扫描trans目录的md文件

transDir = os.path.join(os.getcwd(), 'trans')
corrDir = os.path.join(os.getcwd(), 'corr')

transFiles = list_md_file(transDir)
corrFiles = lsit_md_file(corrDir)
i = 0
fileNum = len(transFiles)
for tfile in transFiles:
    cfile = tfile.replace(transDir,corrDir)
    if (cfile in corrFiles) :
        print('file %s has done'%tfile)
        continue
    
    print('processing %d/%d  %s'%(i,fileNum,tfile))
    correct(file,cfile)
    print('processed %d'%cfile)
