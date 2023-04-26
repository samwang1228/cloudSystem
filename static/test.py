import os
list1=[]
out='top - 17:37:46 up 9:05, 0 users, load average: 1.10, 0.85, 0.60 Tasks: 4 total, 1 running, 3 sleeping, 0 stopped, 0 zombie %Cpu(s): 0.4 us, 0.9 sy, 0.0 ni, 98.6 id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st KiB Mem : 3994724 total, 159844 free, 2787260 used, 1047620 buff/cache KiB Swap: 2097148 total, 1979644 free, 117504 used. 787060 avail Mem PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND 589 root 20 0 326204 33988 10196 S 6.7 0.9 0:00.43 /usr/bin/python3 /cloudSystem/app.py'
output=out.split(' ')
list1.append(output[2])
list1.append(output[4])
print(list1)
print(output)