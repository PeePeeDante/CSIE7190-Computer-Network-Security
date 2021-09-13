#use python2.7 to run this program
import time
import random

def GetSeed():
    t_seed = time.time() * (1<<10)
    t_seed = pow(17, int(t_seed), 0x8d6a6ecc01)
    return t_seed

def Mac(my_nonce, your_nonce):
    return sha256("{},{},{}".format(my_nonce, your_nonce, secret.key))

list_seed = []

for i in range(2000):
    Seed = GetSeed()
    if Seed not in list_seed:
        list_seed.append(Seed)
    #print(Seed)
    time.sleep(0.0001)
    #print(my_Nonce)

file = open("seedsAndNonces.txt","w")
file.write('seeds = [')
for i in list_seed:
    file.write(str(i)+',')
file.write(']\n')

nonces = []
file.write('nonces = [')
for i in list_seed:
    random.seed(i)
    n = random.randint(0,(1<<32))
    nonces.append(n)
nonces.sort()
for n in nonces:
    file.write(str(n)+',')
file.write(']\n')
file.close()

