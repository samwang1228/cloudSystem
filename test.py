import os
list1=[]
for dirPath, dirNames, fileNames in os.walk("C:\\Users\\user\\Desktop\\web\\專題\\flask-web\\main\\static\\uploads\\user"):
    for f in fileNames:
        list1.append(os.path.join(f))
print(list1)