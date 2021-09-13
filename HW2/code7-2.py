from binascii import hexlify, unhexlify
from Crypto.Random import get_random_bytes
from Crypto.Util.number import bytes_to_long
from pwn import *
from Crypto.Cipher import Salsa20
from Crypto.Hash import SHA256, HMAC

def decrypt(key, msg):
    msg = unhexlify(msg.encode())
    nonce = msg[:8]
    c = msg[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.decrypt(c)

# create account
r = remote('cns.csie.org', 10220)
for i in range(5):
    print(r.recvline())
    
r.sendline('1')
r.sendline('Eve')
s = r.recvline()
print(s)
keys = s.decode()[9:-2]
KE_KM = keys.split(', ')
for i in range(2):
    temp = KE_KM[i][1:-1]
    KE_KM[i] = temp
print(KE_KM)

# prepare fakeid_b
fakeid_b = 'Bob'

# initiate connection with alice
r1 = remote('cns.csie.org', 10221)
for i in range(4):
    print(r1.recvline())
    
r1.sendline('1')
s = r1.recvline()
print(s)

nonceAndId_A = s.decode()[2:-1].split('||')

# initiate connection with bob, man in the middle
rb = remote('cns.csie.org', 10222)
for i in range(4):
    print(rb.recvline())
    
rb.sendline('1')
s = rb.recvline()
print(s)

nonceAndId_B = s.decode()[2:-1].split('||')

# prepare man in the middle nonce
fake_nonce_A = nonceAndId_A[0]

# create connection with kdc, man in the middle
r_attack = remote('cns.csie.org', 10220)
for i in range(5):
    print(r_attack.recvline())
    
r_attack.sendline('2')

fakeKX_message = fake_nonce_A+'||'+nonceAndId_B[0]+'||'+'Alice'+'||'+nonceAndId_B[1]
print(fakeKX_message)
r_attack.sendline(fakeKX_message)

s = r_attack.recvline()
print(s)
list_c_t_id_n = s.decode()[9:-2].split(', ')
for i in range(4):
    new_string = list_c_t_id_n[i][1:-1]
    list_c_t_id_n[i] = new_string
    
#print(list_c_t_id_n)



# create connection with kdc
r2 = remote('cns.csie.org', 10220)
for i in range(5):
    print(r2.recvline())
    
r2.sendline('2')

KX_message = nonceAndId_A[0]+'||'+nonceAndId_B[0]+'||'+'Alice'+'||'+'Eve'
print(KX_message)
r2.sendline(KX_message)

s = r2.recvline()
print(s)
Alist_c_t_id_n = s.decode()[9:-2].split(', ')
for i in range(4):
    new_string = Alist_c_t_id_n[i][1:-1]
    Alist_c_t_id_n[i] = new_string
    
#print(Alist_c_t_id_n)

# back to connection with alice
response = Alist_c_t_id_n[0] + '||' + list_c_t_id_n[1] + '||' + 'Bob' + '||' + nonceAndId_B[0]

r1.sendline(response)
for i in range(1):
    print(r1.recvline())
s = r1.recvline()
print(s)

#print(Alist_c_t_id_n[2])

print('test')

print(KE_KM[0])
print("=== KE ===")
print(KE_KM[0])
print(unhexlify(KE_KM[0]))
secret_key = unhexlify(decrypt(unhexlify(KE_KM[0]),Alist_c_t_id_n[2]))

print("=== secret key ===")
print(secret_key)
print("=== secret flag ===")
print(s.decode()[:-1])

#print(util.encrypt(skey, secret.FLAG1))

plaintext = decrypt(secret_key, s.decode()[:-1])
print(plaintext)


