import os
import re
import translators as ts
from listfile import list_md_files
import sys
import getopt

mode = 'file'
debug = ''
path = os.getcwd()
try:
    opts, args = getopt.getopt(sys.argv[1:], 'm:p:d:')
except getopt.GetoptError :
    print('error')

for opt, arg in opts:
    if opt == '-m':
        mode = arg
    elif opt == '-p':
        path = arg
    elif opt == '-d':
        # all : debug all info
        # line : print line and new line 
        # trans : print en an ch
        # form : debug form
        # list : debug list
        debug = arg 

    

def tran_line(en):
    if (len(en) == 0):
        return ''
    
    # en中不能存在&,所以我们把en的&直接去除
    # en中的#号也是没有意义的，不需要翻译
    en = en.replace('&', '')
    en = en.replace('#','')
    en = en.replace('**','')
    en = en.replace('`','')
    en = en.replace('"','')                   
    en = en.replace('\n', ' ')

    len_en = len(en)
    if (len_en > 5000) :
        print('len_en = %d'%len_en)
        print(en)
        ens = en.split('.')
        ch = ''
        for elem in ens:
            ch = ch + ts.google(elem,'en','zh')
        return ch
    while(True) :
        try:
            ch = ts.google(en,'en','zh')
            return '<font color=#00ffff size=3> ' + ch + ' </font>'
        except Exception as e:
            print(en,e)
    
def append_oneline(lines,oneline) :
    if (len(oneline) == 0):
        return
    lines.append(oneline.replace('\n', ' ') + '\n')

def processTitleLine(line):
    # 1. 翻译line成为中文。
    # 2. 英文字段有多少 #，表示是第几级标题，所以中文字段前面也要加上对应的 #
    # 3. 如果英文字段中存在非标题提示符的 ‘#’,这里就会多加#，暂时没有发现这个情况，所以先不处理。
    title = '#################'
    return title[0:line.count('#')] + ' ' + tran_line(line) + ' ' + line.replace('\n',' ')
    
def processNormalLine(line):
    # 普通行 或者 列表行都有可能。
    line_strip = line.strip()
    if(len(line_strip) == 0 ):  return line

    s = len(line) - len(line_strip)
    space = '            '

    # 如果是列表行
    if ((not re.match('\d. ', line_strip) == None) or line_strip.startswith('* ')
            or line_strip.startswith('- ') or line_strip.startswith('+ ')):
        
        line = space[0:s] + '* '  + tran_line(line) + ' ' + line.replace('\n',' ')
        
    else :# 普通行，不做什么处理

        line = space[0:s] + tran_line(line) + ' ' + line.replace('\n',' ')
    
    return line


def delenter(file,newfile):
    with open(file,encoding='utf-8') as file:
        lines = file.readlines()

    str_oneline = ''
    newlines = []
    codeline = False
    formline = False

    num = 1
    for line in lines:
        line_strip = line.strip()

        # print('line %d/%d'%(num,len(lines)))
        print('line %d/%d'%(num,len(lines)),end='\r')
        num = num + 1
        # 判断当前是否处于codeline模式
        if (line_strip.startswith('```')):
            codeline = not codeline
            append_oneline(newlines,line)
            continue
        
        # 处于codeline 状态的时候我们不处理里面的行
        if (codeline):
            append_oneline(newlines,line)
            continue

        # 如果某一行都是空格，表示分段，这个时候把前面的行数据组合起来当成一个新行append，本行也直接append
        if (len(line_strip) == 0):
            # str_oneline = tran_line(str_oneline) + ' ' + str_oneline + ' \n'
            str_oneline = processNormalLine(str_oneline)
            append_oneline(newlines,str_oneline)
            #  append_oneline(newlines,str_oneline.replace('\n', ' ') + '\n')
            append_oneline(newlines,line)
            str_oneline = ''
            continue

        # #开头表示是标题行，标题行只占一行
        if (line_strip.startswith('#')) :

            # 标题行前面应该都是属于普通行，直接翻译后合并即可
            # str_oneline = tran_line(str_oneline) + ' ' + str_oneline + ' \n'
            str_oneline = processNormalLine(str_oneline)
            append_oneline(newlines,str_oneline)
            
            # 处理标题行，标题行需要在中文前面 + 对应的标题数
            line = processTitleLine(line)
            append_oneline(newlines,line)
            str_oneline = ''
            continue

        # 当前行是list的首行，那么前面的数据可以当成一段，本行当作新一行的起始数据
        if ((not re.match('\d. ', line_strip) == None) or line_strip.startswith('* ')
            or line_strip.startswith('- ') or line_strip.startswith('+ ')):
            
            # 当前行是list，前面的是list行或者普通行，但是和本行肯定无关，所以直接翻译后合并
            str_oneline = processNormalLine(str_oneline)
            append_oneline(newlines,str_oneline)

            str_oneline = line
            continue

        # 存在| 表示当前行是表格行
        if(debug == 'form'):
            print('formline = ' ,formline)
            print(line_strip)
        if ('|' in line_strip):
            formline = True
            print('into  | form line')
            if (not len(str_oneline) == 0 ):
                # str_oneline = tran_line(str_oneline) + ' ' + str_oneline + ' \n'
                str_oneline = processNormalLine(str_oneline)
                append_oneline(newlines, str_oneline)

            str_oneline = ''
            # 如果当前行是 | :------|形式
            if(debug == 'form'):print(len(line))
            if(line.count('|') + line.count(' ') + line.count(':') + line.count('-') + line.count('\n')== len(line)) :
                append_oneline(newlines,line)
                continue

            # 把当前行以|分割，然后翻译
            elems = line.split('|')
            new = '| '
            for elem in elems:
                print(elem,len(elem))
                newelem = elem.strip()
                if ( not len(newelem) == 0 ):
                    
                    # if(newelem.count('-') == len(newelem))
                    new = new + tran_line(elem) + ' ' + elem + ' | '
                    # new  = new + elem + ' | '
                    # print(new)

                elif (not len(elem) == 0):
                    if(not elem == '\n'):
                        new  = new + elem + ' |'

                if(debug =='form'):print(new)
            
            append_oneline(newlines, new)
            if(debug == 'form'): print('str_oneline',str_oneline)
            continue

        elif(formline and line_strip.startswith(':')) :
            # 处于formline模式，冒号开头表示也是formline
            if(debug == 'form'): print('into : form line')
            # 把当前行以:分割，然后翻译
            elems = line.split(':')
            new = '| '
            for elem in elems:
                if(debug == 'form'): print(elem,len(elem))
                newelem = elem.strip()
                if ( not len(newelem) == 0 ):
                    
                    # if(newelem.count('-') == len(newelem))
                    new = new + tran_line(elem) + ' ' + elem + ' | '
                    # new  = new + elem + ' | '
                    # print(new)

                elif (not len(elem) == 0):
                    if(not elem == '\n'):
                        new  = new + elem + ' |'

                if(debug == 'form'): print(new)
            
            if (not len(str_oneline) == 0):
                # str_oneline = tran_line(str_oneline) + ' ' + str_oneline + ' \n'
                str_oneline = processNormalLine(str_oneline)
                append_oneline(newlines,str_oneline)
                str_oneline = ''
            append_oneline(newlines,new)
            continue
        else :
            formline = False
            if(debug == 'form'):
                print('leave form line')

        if (len(str_oneline) == 0):
            str_oneline = line
        else :
            str_oneline = str_oneline  + line_strip
 
    if(not len(str_oneline) == 0) :
        str_oneline = processNormalLine(str_oneline)
        append_oneline(newlines,str_oneline)
        str_oneline = ''


    with open(newfile,mode='w',encoding='utf-8') as newfile :
        newfile.writelines(newlines)

if (mode == 'dir'):
    allfiles = list_md_files(path)
    cwd = path
    transpath = os.path.join(path,'trans\\')
    if not os.path.isdir(transpath):
        os.makedirs(transpath)
    
    
    print(path)
    print(transpath)

    newfiles = list_md_files(transpath)
    
    files = []
    for file in allfiles:
        if not file in newfiles:
            files.append(file)
    
    i = 0
    for file in files:
        i = i + 1
        newfile = file.replace(cwd,transpath)
        newdir = os.path.split(newfile)
        if not os.path.isdir(newdir[0]):
            os.makedirs(newdir[0])
        if (newfile in newfiles) :
            print('escape ' + str(file))
            continue
        if (file in newfiles) :
            continue
        print('processing ' + str(i) + '/' + str(len(files)) + ' ' + str(file))
    
        delenter(file,newfile)
        print('processed ' + str(newfile))
else :
    delenter(path,path+'new.md')
