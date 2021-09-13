# preparing constants and read files
file_D1 = open('D1.txt','r')
file_D2 = open('D2.txt','r')
file_D3 = open('D3.txt','r')
files = [file_D1,file_D2,file_D3]

D1_data = []
D2_data = []
D3_data = []
data = [D1_data,D2_data,D3_data]

for i in range(3):
    for lines in files[i]:
        data[i].append(int(lines[2:]))

constants = []  # p, q, g, c0, c1, c2
file_parameter = open('parameter.txt', 'r')

for lines in file_parameter:
    constants.append(int(lines[4:]))

p = constants[0]
q = constants[1]
g = constants[2]
c0 = constants[3]
c1 = constants[4]
c2 = constants[5]

import math

def modularPower(base,power,mod):
    if power == 1:
        return base
    if power == 0:
        return 1
    b = base
    iter = int(math.log2(power))
    for i in range(iter):
        b = (b**2)%mod
    return (b * modularPower(base,power-2**iter,mod))%mod

# find d1, d2, d3
d1 = None
m1 = [c0,c1,c2]
M1 = 1
for num in m1:
    M1 = M1*(num%p)
    M1 = M1%p
for data in D1_data:
    temp = data%q
    if M1 == modularPower(g,temp,p):
        print(data)
        d1 = data
        break

d2 = None
m2 = [c0,c1,c1,c2,c2,c2,c2]
M2 = 1
for num in m2:
    M2 = M2*(num % p)
    M2 = M2 % p
for data in D2_data:
    temp = data % q
    if M2 == modularPower(g, temp, p):
        print(data)
        d2 = data
        break

d3 = None
m3 = [c0, c1, c1, c1, c2, c2, c2, c2,c2,c2,c2,c2,c2]
M3 = 1
for num in m3:
    M3 = M3*(num % p)
    M3 = M3 % p
for data in D3_data:
    temp = data % q
    if M3 == modularPower(g, temp, p):
        print(data)
        d3 = data
        break

# compute a0
a0 = (3*d1 - 3*d2 + d3)%q

f = open('problem5.txt','w')
f.write('D1 = ')
f.write(str(d1)+'\n')
f.write('D2 = ')
f.write(str(d2)+'\n')
f.write('D3 = ')
f.write(str(d3)+'\n')
f.write('a0 = ')
f.write(str(a0)+'\n')
f.close()

for i in range(3):
    files[i].close()
file_parameter.close()
