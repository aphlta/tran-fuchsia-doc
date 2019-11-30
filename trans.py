import os
import re
import translators as ts
from listfile import list_md_files

def tran_line(en):
    if (len(en) == 0):
        return ''
    
    # en中不能存在&,所以我们把en的&直接去除
    # en中的#号也是没有意义的，不需要翻译
    en = en.replace('&', '')
    en = en.replace('#','')
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

    return ts.google(en,'en','zh')

def append_oneline(lines,oneline) :
    if (len(oneline) == 0):
        return
    lines.append(oneline.replace('\n', ' ') + '\n')

def delenter(file,newfile):
    with open(file,encoding='utf-8') as file:
        lines = file.readlines()

    str_oneline = ''
    newlines = []
    codeline = False

    num = 1
    for line in lines:
        line_strip = line.strip()

        # print('line %d/%d'%(num,len(lines)))
        print('line %d/%d'%(num,len(lines)),end='\r')
        num = num + 1
        # 判断当前是否处于codeline模式
        if (line_strip.startswith('```')):
            codeline = not codeline
            newlines.append(line)
            continue
        
        # 处于codeline 状态的时候我们不处理里面的行
        if (codeline):
            newlines.append(line)
            continue

        # 如果某一行都是空格，表示分段，这个时候把前面的行数据组合起来当成一个新行append，本行也直接append
        if (len(line_strip) == 0):
            str_oneline = str_oneline + ' ' +  tran_line(str_oneline)
            append_oneline(newlines,str_oneline)
            # newlines.append(str_oneline.replace('\n', ' ') + '\n')
            newlines.append(line)
            str_oneline = ''
            continue

        # #开头表示是标题行，标题行只占一行
        if (line_strip.startswith('#')) :
            str_oneline = str_oneline + ' ' +  tran_line(str_oneline)
            append_oneline(newlines,str_oneline)
            # newlines.append(str_oneline.replace('\n', " ") + '\n')
            line = line.replace('\n',' ') + ' ' + tran_line(line)
            newlines.append(line)
            str_oneline = ''
            continue

        # 当前行是list的首行，那么前面的数据可以当成一段，本行当作新一行的起始数据
        if ((not re.match('\d. ', line_strip) == None) or line_strip.startswith('* ')
            or line_strip.startswith('- ') or line_strip.startswith('+ ')):
            str_oneline = str_oneline + ' ' +  tran_line(str_oneline)
            append_oneline(newlines,str_oneline)
            # newlines.append(str_oneline.replace('\n', ' ') + '\n') 
            str_oneline = line
            continue

        if (len(str_oneline) == 0):
            str_oneline = line
        else :
            str_oneline = str_oneline  + line_strip
 
    with open(newfile,mode='w',encoding='utf-8') as newfile :
        newfile.writelines(newlines)


files = list_md_files(os.path.join(os.getcwd(),'fuchsia-master-docs'))
cwd = os.getcwd()
transpath = os.path.join(cwd,'trans')
newfiles = list_md_files(transpath)
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
    print('processing ' + str(i) + '/' + str(len(files)) + ' ' + str(file))
   
    delenter(file,newfile)
    print('processed ' + str(newfile))

# delenter(r'C:\mwm\error.md',r'C:\mwm\new_error.md')