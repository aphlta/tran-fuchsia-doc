import os
from trans import list_md_files

correctDict = {'fuchsia':'紫红色'}
def correctFile(file,newfile):
    with open(file,encoding='utf-8') as file:
        lines = file.readlines()
    newlines = []
    for line in lines:
        for key in correctDict.keys():
            if(key in line):
                newline = line.replace(correctDict[key],key)
                newlines.append(newline)
    
    with open(newfile,mode='w',encoding='utf-8') as newfile:
        newfile.writelines


# files = list_md_files(os.getcwd(), 'trans')
# transDir = os.path.join(os.getcwd(),'trans')
# files = list_md_files(transDir)
# correctDir = os.path.join(os.getcwd(),'correct')
# correctFiles = list_md_files(correctDir)
# i = 0
# for file in files:
#     i = i + 1
#     newfile = file.replace(transDir,correctDir)
#     newdir = os.path.split(newfile)
#     if not os.path.isdir(newdir[0]):
#         os.makedirs(newdir[0])
#     if (newfile in correctFiles) :
#         print('escape ' + str(file))
#         continue
#     print('processing ' + str(i) + '/' + str(len(files)) + ' ' + str(file))
#     correctFile(file,newfile)

correctFile(r'C:\mwm\my.md',
            r'C:\mwm\mycorect.md')