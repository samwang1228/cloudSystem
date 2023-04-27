import random
import os
f = open(os.path.join('test.txt'),encoding='utf-8')
cnt=0
info=[]
ryric=''
for line in f.readlines():
    cnt+=1
    if(cnt>=4):
        ryric+=str(line)
    info.append(line)
print(info[2])
picUrl=str(info[2])
picUrl[6:len(picUrl)-1]
print(ryric)
print(picUrl[6:len(picUrl)-1])