#use python3.6 to run the following code
from Nonces import nonces
BA_nonce = nonces[0]
MAC_DICT1 = {} # {N0:(N0,N0),N1:(N1,N0),...,N128:(N128,N0)}

from pwn import *

while len(MAC_DICT1) < 128:
    r = remote('cns.csie.org', 10225)
    for i in range(5):
        print(r.recvline())

    r.sendline(str(BA_nonce))
    print(str(BA_nonce))

    for i in range(6): #7,8
        print(r.recvline())
    
    line_key = r.recvline()
    print(line_key)
    key = int(line_key.decode()[-11:-1])
    
    line_mac = r.recvline()
    print(line_mac)
    mac = line_mac.decode()[-65:-1]
    
    if not key in MAC_DICT1:
        MAC_DICT1[key] = mac
    
    for i in range(3):
        print(r.recvline())
        
    cipher = ""
    r.sendline(cipher)

    for i in range(8):
        print(r.recvline())

print(MAC_DICT1)

FINAL_ATTACK = nonces[1]

found = False
while(not found):
    r = remote('cns.csie.org', 10225)
    for i in range(5):
        print(r.recvline())

    r.sendline(str(FINAL_ATTACK))
    print(str(FINAL_ATTACK))

    for i in range(6): #7,8
        print(r.recvline())

    line_key = r.recvline()
    print(line_key)
    key = int(line_key.decode()[-11:-1])

    line_mac = r.recvline()
    print(line_mac)
    mac = line_mac.decode()[-65:-1]
    print(mac)

    for i in range(3):
        print(r.recvline())

    if key == BA_nonce:
        cipher = MAC_DICT1[FINAL_ATTACK]
        r.sendline(cipher)
        found = True
        for i in range(9):
            print(r.recvline())
    else:
        r.sendline("")
        for i in range(8):
            print(r.recvline())
