import re
import operator
import csv
import difflib
keyofpattern = []
diclist =  []
dicpattern = {}
listkey = []
typekeylist = []
methodpatterstr = '[a-zA-Z0-9_\.]+\(.*?\)'
methodpatterstr1 = '[a-zA-Z0-9_\.]+<.*?>\(.*?\)'
strpatterstr = '".*?"'
charpatterstr = "'.*?'"
numpatternstr = '[0-9]+'
objectpatternstr = '[A-Z][A-Za-z_0-9\[\]]*'
symbelpatternstr = '\+\+|--|\[\]|\-\>|\&\&|\|\||==|!=|<=|>=|^=|\|=|[^A-Za-z0-9 ]'
variblepatternstr = '[a-z_][A-Za-z0-9\._\[\]]*'
variblepatternstr1 = '[a-z][A-Z0-9\._\[\]]+'
patternstr = '('+ strpatterstr+'|'+charpatterstr+'|'+methodpatterstr+'|'+methodpatterstr1+'|'+'[A-Za-z0-9\._\[\]]+' + '|'+objectpatternstr+'|'+numpatternstr+'|'+symbelpatternstr+')'
path = '/Volumes/文档/大学/大学学习/大二下/冯如杯/SampleCode_2/File'
def getdicpattern(rawline):
    if '@' in rawline:
        return
    line = seperates(rawline)
    l = ''
    k = 0
    #'([]|".*"|\'.*\'|->|\&\&|\|\||==|!=|[A-Za-z0-9._]+|\+\+|--|[^A-Za-z0-9])'
    resultunit = re.findall(patternstr,line)
    #print (resultunit)
    for x in resultunit:
        xc = classify(x,l)
        if xc != '':
            l += xc + ' '
    #l = l.replace('( )','( $$ )')
    #print(rawline.strip())
    #print(l+'\n')
    '''
    if '!!! + ,' in l:
        print(rawline)
        print(l)
        #print(resultunit)
    '''
    return l
def seperates(s):
    line = s.replace('\n','')
    line = line.replace(' (','(')
    line = line.replace('\t','')
    line = line.replace('"',' "')
    line = line.replace('if(','if (')
    line = line.replace('for(','for (')
    line = line.replace(' [','[')
    line = line.replace('while(','while (')
    line = line.replace('switch(','switch (')
    line = line.replace('synchronized(','synchronized (')
    line = line.replace('return','return ')
    line = re.sub(strpatterstr,'"x"',line)
    line = re.sub(charpatterstr,'"x"',line)
    if 'System.out.println' in line:
        line = 'System.out.println();'
    line = line.strip()
    line = cleanmethod(line)
    return line
def classify(x,l):
    if (x==' '):
        return ''
    elif re.fullmatch(strpatterstr,x):
        return '!!!'
    elif re.fullmatch(charpatterstr,x):
        return '!!!'
    elif re.fullmatch(methodpatterstr1,x) and 'if' not in x:
        if len(l) > 2 and l[-2] == '~':
            return ''
        return '~~~'
    elif re.fullmatch(methodpatterstr,x):
        if len(l) > 2 and l[-2] == '~':
            return ''
        return '~~~'
    elif re.fullmatch(numpatternstr,x):
        return '!!!'
    elif x in typekeylist:
        return '###'
    elif x in listkey:
        return x
    elif re.fullmatch(objectpatternstr,re.sub('[A-Za-z0-9]+\.','',x)):
        if len(l) > 2 and l[-2] == '#':
            return '$$$'
        return '###'
    elif re.fullmatch(objectpatternstr+'\[\]',re.sub('[A-Za-z0-9]+\.','',x)):
        if len(l) > 2 and l[-2] == '#':
            return '$$$'
        return '###'
    elif re.fullmatch(variblepatternstr1,re.sub('[A-Za-z0-9]+\.','',x)):
        return '$$$'
    elif re.fullmatch(variblepatternstr,re.sub('[A-Za-z0-9]+\.','',x)):
        return '$$$'
    else:
        return '$$$'
def cleanmethod(s):
    start = 0
    end  = 0
    deep = 0
    for i in range(1,len(s)):
        if s[i] == ')':
            if deep == 1:
                end = i
                s = s[:start+1]+'@'*(end-start-1)+s[end:]
            if deep>0:
                deep -= 1
        if s[i] == '(' and s[i-1]!=' ':
            if deep == 0:
                start = i
            deep += 1
    s = s.replace('@','')
    return s
def addl(l,dic):
    if l in dic.keys():
        dic[l] += 1
    else:
        dic[l] = 1
def main1():
    file = open('newkey2.txt','r')
    l1 = file.readlines()
    for line in l1:
        listkey.append(line.split(' ')[0])
    file2 = open('typekey.txt','r')
    l1 = file2.readlines()
    for line in l1:
        typekeylist.append(line.split(' ')[0].strip())
    #print(listkey)
    for i in range(18000):
        f = open(path + str(i) + '.txt','r')
        linelist = f.readlines()
        read = True
        for line in linelist:
            if '/*' in line:
                read = False
            if read==True:
                if '//' not in line:
                    addl(getdicpattern(line),dicpattern)
            if '*/' in line:
                read = True
        if i % 100 == 0:
            print(i)
    listpattern = sorted(dicpattern.items(),key=lambda x:x[1],reverse = True)
    #print(listpattern[:10])
    #for u in listpattern[:100]:
        #print(u)
    with open('frepattern3.csv', 'w') as f:
        writer = csv.writer(f)
        for row in listpattern[:]:
            #print(str(row[0]))
            f.write(str(row[0])+','+str(row[1])+'\n')
            #writer.writerow(row)
            #print(row)
def getscore(p,c):
    return difflib.SequenceMatcher(None,p,c).ratio()
def getpattern():
    f = open('/Volumes/文档/大学/大学学习/大二下/PythonSupporting/PythonSupportingPackage/sortedfp3.csv','r')
    rawlist = f.readlines()
    newlist = []
    for x in rawlist:
        s = ''
        for i in range(len(x.split(' '))-1):
            s = s + x.split(' ')[i] +' '
        newlist.append(s.strip())
    return newlist
def simsybl(s):
    return s.replace('###','#').replace('$$$','$').replace('~~~','~').replace('!!!','!')
def linetonum(diclist,line,rawline):
    score = 0.0
    index = 0
    for i in range(len(diclist)):
        if getscore(line,diclist[i])>score:
            score =  getscore(simsybl(line),simsybl(diclist[i]))
            #print (score)
            index = i
    if score < 0.7:
        print(rawline)
        print(line)
        print(score)
        print(diclist[index])
        print('\n-------------------------------------------------\n')
    return index
def main2():
    file = open('newkey2.txt','r')
    l1 = file.readlines()
    for line in l1:
        listkey.append(line.split(' ')[0])
    file2 = open('typekey.txt','r')
    l1 = file2.readlines()
    for line in l1:
        typekeylist.append(line.split(' ')[0].strip())
    diclist = getpattern()
    writelist = []
    for i in range(18000):
        f = open(path + str(i) + '.txt','r')
        linelist = f.readlines()
        read = True
        l = ''
        for line in linelist:
            if '/*' in line:
                read = False
            if read==True:
                if '//' not in line and '@' not in line:
                    #print(line)
                    l += str(linetonum(diclist,getdicpattern(line).strip(),line))+' '
            if '*/' in line:
                read = True
        writelist.append(l.strip())
        if i % 1 == 0:
            print(i)
    fw = open('codetonum.txt','w')
    for l in writelist:
        fw.write(l+'\n')
def main3():
    file = open('newkey2.txt','r')
    l1 = file.readlines()
    for line in l1:
        listkey.append(line.split(' ')[0])
    fw = open('codetonum3.txt','w')
    file2 = open('typekey.txt','r')
    l1 = file2.readlines()
    for line in l1:
        typekeylist.append(line.split(' ')[0].strip())
    diclist = getpattern()
    for i in range(len(diclist)):
        unitlist = []
        unitlist.append(diclist[i])
        vardic = {}
        constdic = {}
        typedic = {}
        methdic = {}
        unitlist.append(vardic)
        unitlist.append(constdic)
        unitlist.append(typedic)
        unitlist.append(methdic)
        keyofpattern.append(unitlist)
    for i in range(18000):
        f = open(path + str(i) + '.txt','r')
        linelist = f.readlines()
        read = True
        for line in linelist:
            if '/*' in line:
                read = False
            if read==True:
                if '//' not in line and '@' not in line:
                    searchkeyword(line,diclist)
            if '*/' in line:
                read = True
        if i % 100 == 0:
            print(i)
    f = open('keyofpattern3.txt','w')
    for i in range(len(keyofpattern)):
        f.writelines(keyofpattern[i][0]+'\n')
        for j in range(4):
            keysortlist = sorted(keyofpattern[i][j+1].items(),key=lambda x:x[1],reverse = True)
            #print('\n'.join(keysortlist[k][0]for k in range(len((keysortlist)))))
            x = 15
            if len(keysortlist) < 15:
                x = len(keysortlist)
            f.writelines(str(j)+':'+' '.join((keysortlist[k][0]+','+str(keysortlist[k][1]))for k in range(x)))
            f.writelines('\n') 
            #f.writelines('\n---------------------\n')
        f.writelines('\n')    
def searchkeyword(rawline,diclist):
    if '@' in rawline:
        return
    line = seperates(rawline)
    thispattern = getdicpattern(line).strip()
    if thispattern not in diclist:
        return
    resultunit = re.findall(patternstr,line.strip())
    index = diclist.index(thispattern)
    for x in resultunit:
        if x[0] == '.':
            continue
        y = classify(x,'')
        if y == '':
            continue
        elif y == '$$$':
            addl(x,keyofpattern[index][1])
        elif y == '###':
            addl(x,keyofpattern[index][2])
        elif y == '~~~':
            x = re.findall('[a-zA-Z0-9.]+',x)[0]
            addl(x,keyofpattern[index][3])
        elif y == '!!!':
            addl(x,keyofpattern[index][4])
def main4():
    file = open('newkey2.txt','r')
    l1 = file.readlines()
    for line in l1:
        listkey.append(line.split(' ')[0])
    file2 = open('typekey.txt','r')
    l1 = file2.readlines()
    for line in l1:
        typekeylist.append(line.split(' ')[0].strip())
    diclist = getpattern()
    f = open('/Volumes/文档/大学/大学学习/大二下/冯如杯/SampleCode_2/File1.txt','r')
    linelist = f.readlines()
    read = True
    l = ''
    for line in linelist:
        if '/*' in line:
            read = False
        if read==True:
            if '//' not in line and '@' not in line:
                #print(line)
                l += str(linetonum(diclist,getdicpattern(line).strip(),line))+' '
        if '*/' in line:
            read = True
    print(l)
file = open('/Volumes/文档/大学/大学学习/大二下/PythonSupporting/PythonSupportingPackage/newkey2.txt','r')
l1 = file.readlines()
for line in l1:
    listkey.append(line.split(' ')[0])
fw = open('codetonum.txt','w')
file2 = open('/Volumes/文档/大学/大学学习/大二下/PythonSupporting/PythonSupportingPackage/typekey.txt','r')
l1 = file2.readlines()
for line in l1:
    typekeylist.append(line.split(' ')[0].strip())
diclist = getpattern()
if __name__== "__main__":
    mod = input()
    if mod == '1':
        main1()
    elif mod == '2':
        main2()
    elif mod == '3':
        main3()
    elif mod == '4':
        main4()
    else:
        print('exit')