from listfile import list_src_files
import os
import translators as ts


srcs = list_src_files(r'Z:\myfuchsia\zircon')
outpath = r'Z:\myfuchsia\trans'

def getwhites(str):
    count = 0 
    for s in str:
        if (s == ' '): count = count + 1
        else : break
    return count

for src in srcs:
    outfile = src.replace(r'Z:\myfuchsia',r'Z:\myfuchsia\trans')
    newdir = os.path.split(outfile)
    if not os.path.isdir(newdir[0]):
        os.makedirs(newdir[0])

    if (os.path.exists(outfile)) : continue

    with open(src,encoding='utf-8') as file:
        lines = file.readlines()

    comment = ''
    state = False
    whites = 0
    newlines = []
    zh_comment = ''
    for line in lines:
        line_strip = line.strip()
        # 当前行是注释行
        
        
        if (line_strip.startswith('//')):
            comment = comment + line_strip.replace('//','').replace('\n',' ')
            whites = getwhites(line)
            state = True
            if (len(comment) > 2000):
                if(whites == 0) : zh_comment = '// ' + ts.google(comment,'en','zh') + '\n'
                else:             zh_comment ='          '[0:whites] + '// ' + ts.google(comment,'en','zh') + '\n'
                comment = ''
        else:
            if ( not len(comment) == 0):
                # print(src)
                # print(comment)
                if (not 'BSD-style license' in comment):
                    if(whites == 0) : zh_comment = '// ' + ts.google(comment,'en','zh') + '\n'
                    else:             zh_comment ='          '[0:whites] + '// ' + ts.google(comment,'en','zh') + '\n'
                comment = ''
            state = False

        if (not len(zh_comment) == 0) :
            newlines.append(zh_comment)
            zh_comment = ''

        newlines.append(line)
        
        
    # print(newlines)
    outfile = src.replace(r'Z:\myfuchsia',r'Z:\myfuchsia\trans')
    newdir = os.path.split(outfile)
    if not os.path.isdir(newdir[0]):
        os.makedirs(newdir[0])
    with open(outfile,mode='w',encoding='utf-8') as out:
        out.writelines(newlines)

