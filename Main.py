import time
import sys
import re
import numpy as np
from PythonSupportingPackage.Vectors import vectors
from PythonSupportingPackage.Newpre import newpre
from PythonSupportingPackage.makepattern import *
def readinput():
    str=""
    while True:
        s = input()
        if '@' in s or '//' in s:
            continue
        if s=="###":
            return str.strip()
        if s.replace(' ','').replace('\t','')!='':
            str = str + s + '\n'
dim = 500
modelname = '/Volumes/文档/大学/大学学习/大二下/PythonSupporting/PythonSupportingPackage/model3top10'
#path = sys.argv[2]+'/CodeCommendPy/'
path = '/Users/huangjihui/IdeaProjects/CodeRecommendPythonPackage/CodeCommendPy/'
#f = open("/Volumes/文档/大学/大学学习/大二下/PythonSupporting/PythonSupportingPackage/teststr.txt","r")
#txt = f.read().strip()
txt = readinput()
#print(txt)
print('success')
#print('last\n'+txt[-10:].replace('\n',' '))
txtlist = txt.split('\n')[-10:]
txtnumlist = []
dic = getpattern()
for x in txtlist:
    #print(stringToNumber(x))
    #print(x)
    #print(dic[linetonum(getpattern(),getdicpattern(x).strip(),x.strip())])
    txtnumlist.append(linetonum(dic,getdicpattern(x).strip(),x.strip()))
'''
for x1 in txtnumlist:
    print(' '.join(patternset2[x1-1]))
'''
#print(txtnumlist)
x = np.array([vectors(txtnumlist,dim)])
yprelist,yprescore= newpre(10,dim,modelname,x)
i = 0
for y in yprelist:
    print(diclist[y]+'\n'+str(round(yprescore[i]*100,1)).rjust(5,'#')+'    ')
    i += 1