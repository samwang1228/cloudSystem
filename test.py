import random
import time
t=time.time()
r=random.randrange(0, 101, 2)
filepath='/share/' + str(t)  +str(r)
print(filepath)