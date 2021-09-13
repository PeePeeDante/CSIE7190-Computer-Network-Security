from pwn import *
from binascii import unhexlify

def xor(a, b):
    if a > b:
        x = bin(a)[2:]
        y = bin(b)[2:]
    else:
        x = bin(b)[2:]
        y = bin(a)[2:]
    while len(x) > len(y):
        y = '0' + y
    result = ''
    for i in range(len(x)):
        if x[i] != y[i]:
            result += '1'
        else:
            result += '0'
    return int(result, 2)

r = remote('cns.csie.org', '10202')
token = '796f75725f65766572796461795f6976254d096f3657ed543d5b6ee7d22ba586abd9e0e19e311efafd1e1c73b495852e19be85e7afd1f8b5a7e0f7db79cb6c6b4452aa7916d9ad9b9f35e34098aef66e101a2d9f3bc2a070820c62a98fdf4de5ac58236cb5ccd4a0c4fdad7646d0c104'
blocks = int(len(token)/32)

##### process flow #####
for i in range(5):
    print(r.recvline())

print('1. get token')    
r.sendline('1')

for i in range(6):
    print(r.recvline())

test = '796f75725f65766572796461795f6976254d096f3657ed543d5b6ee7d22ba586abd9e0e19e311efafd1e1c73b495852e19be85e7afd1f8b5a7e0f7db79cb6c6b4452aa7916d9ad9b9f35e34098aef66e101a2d9f3bc2a070820c62a98fdf4de5ac58236cb5ccd4a0c4fdad7646d0c104'
'''
guess_16 = '02'
element_16 = test[32*(blocks-1)-2:32*(blocks-1)]
element_16 = hex(xor(xor(int(element_16,16),int(guess_16,16)),3))[2:]
while len(element_16) < 2:
    element_16 = '0' + element_16
guess_15 = '02'
element_15 = test[32*(blocks-1)-4:32*(blocks-1)-2]
element_15 = hex(xor(xor(int(element_15, 16), int(guess_15, 16)), 3))[2:]
while len(element_15) < 2:
    element_15 = '0' + element_15
'''
hexa_list = []
for i in range(16):
    hexa_list.append(hex(i)[2:])

print('wait')

guess_msg = [None] * 16
guess_msg[14], guess_msg[15] = '02','02'
for block_index in range(13, -1, -1):
    switch = False
    for k in range(16):
        for j in range(16):
            new_token = ''
            guess_msg[block_index] = hexa_list[k] + hexa_list[j]

            element = [None]*(16-block_index)
            for m in range(16-block_index):
                e = test[32*(blocks-1)-(m+1)*2:32*(blocks-1)-m*2]
                e = hex(xor(xor(int(e, 16), int(guess_msg[16-m-1], 16)), 16-block_index))[2:]
                while len(e) < 2:
                    e = '0' + e
                element[16-block_index-m-1] = e    
            concate_e = ''
            for e in element:
                concate_e += e

            new_token = test[:32*(blocks-1)-(16-block_index)*2] + \
                concate_e + test[32*(blocks-1):]

            #print('2. login')
            r.sendline('2')
            r.sendline(new_token)
            response = r.recvline()
            #print(response)
            #print(response.decode())

            if (response.decode()[62] != 'P'):
                #print(guess_msg[block_index])
                switch = True
                if switch == True:
                    for i in range(5):
                        r.recvline()
                    break
            for i in range(5):
                r.recvline()
        if (switch):
            break
last_block = ''
for guess in guess_msg:
    last_block += guess
#print(last_block)

ctf = ''
ctf_1 = unhexlify(last_block).decode()

all_blocks = [None]*7
for i in range(6):
    all_blocks[i] = [None]*16
all_blocks[6] = guess_msg

for l in [5,4,3,2]:
    for block_index in range(15, -1, -1):
        switch = False
        for k in range(16):
            for j in range(16):
                new_token = ''
                all_blocks[l][block_index] = hexa_list[k] + hexa_list[j]

                element = [None]*(16-block_index)
                for m in range(16-block_index):
                    e = test[32*l-(m+1)*2:32*l-m*2]
                    e = hex(
                        xor(xor(int(e, 16), int(all_blocks[l][16-m-1], 16)), 16-block_index))[2:]
                    while len(e) < 2:
                        e = '0' + e
                    element[16-block_index-m-1] = e
                #print(all_blocks[l])
                #print(element)
                concate_e = ''
                for e in element:
                    concate_e += e

                new_token = test[:32*l-(16-block_index)*2] + \
                    concate_e + test[32*l:32*(l+1)]

                #print('2. login')
                r.sendline('2')
                r.sendline(new_token)
                response = r.recvline()
                #print(response)
                #print(response.decode())

                if (response.decode()[62] != 'P'):
                    #print(all_blocks[l][block_index])
                    switch = True
                    if (switch):
                        for i in range(5):
                            r.recvline()
                        break
                for i in range(5):
                    r.recvline()
            if (switch):
                break
    last_block = ''
    for guess in all_blocks[l]:
        last_block += guess
    ctf_1 = unhexlify(last_block).decode() + ctf_1

print('done')
print(ctf_1)
f = open('problem6.txt', 'a')
f.write(ctf_1)
f.close()
