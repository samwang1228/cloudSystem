import random
import os
lr=[]
url=[]
f = open('data.txt','r')
for line in f.readlines():
    lr.append(line[0:line.find('https')])
    url.append(line[line.find('http'):len(line)-1])
print(lr)
print(url)