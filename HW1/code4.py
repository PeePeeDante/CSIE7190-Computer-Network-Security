from pwn import *

def caesar(key,string,key_increment=0):
    sol = ''
    for i in range(len(string)):
        if ord(string[i]) >= 97 and ord(string[i]) <= 122:
            sol += chr((ord(string[i])-key-97)%26 + 97)
        elif ord(string[i]) >= 65 and ord(string[i]) <= 90:
            sol += chr((ord(string[i])-key-65)%26 + 65)
        else:
            sol += string[i]
    return sol

#returns position of target character
def linearSearch(char, message):
    for i in range(len(message)):
        if ord(message[i]) == (ord(char)+1):
            return i
    return -1

class captureFlag:
    def __init__(self, r, p=''):
        self.r = r
        self.p = p

    def getLineToString(self):
        self.p = str(self.r.recvline())
        print(self.p)

    def request(self, rowsCorrect=0):
        for i in range(8-rowsCorrect):
            print(self.r.recvline())
        self.getLineToString()

    def sol_1(self):
        solution = self.p[7:-3]
        print(solution)
        self.r.sendline(solution)
        
    def sol_2(self):
        temp = self.p[11:-3]
        solution = caesar(13,temp)
        print(self.r.recvline())
        print(solution)
        self.r.sendline(solution)

    def sol_3(self):
        cipher_1 = self.p[11:-3]
        self.getLineToString()
        msg_1 = self.p[11:-3]
        key = ord(cipher_1[0])-ord(msg_1[0])

        self.getLineToString()
        temp = self.p[11:-3]
        
        solution = caesar(key,temp)
        print(self.r.recvline())
        print(solution)
        self.r.sendline(solution)

    def sol_4(self):
        temp = self.p[11:-3]
        accept = ''
        i = 0
        
        while(True):
            solution = caesar(i,temp)
            print(solution)
            accept = input('[y]/n: ')
            if chr(accept[0]) == 'y':
                self.r.sendline(solution)
                break
            i = (i+1) % 26
            
    def sol_5(self):
        self.p = self.r.recvuntil('m2 = ?\n').decode()
        print(self.p)
        
        statements = []
        dic = {}
        useful = {'m1':'','c1':'','c2':'','m2':''}
        pos_1_char = -1
        pos_2_char = -1
        char_1 = ''
        
        statements = self.p.splitlines()
        for comp in statements:
            if comp.find('m1') != -1:
                useful['m1'] = comp[comp.find('=')+2:]
            elif comp.find('c1') != -1:
                useful['c1'] = comp[comp.find('=')+2:]
            elif comp.find('c2') != -1:
                useful['c2'] = comp[comp.find('=')+2:]
                
        for i in range(len(useful['m1'])):
            if ord(useful['m1'][i]) >= 97 and ord(useful['m1'][i]) <= 122:
                pos_1_char = i
                pos_2_char = linearSearch(useful['m1'][pos_1_char], useful['m1'])
                if pos_2_char != -1:
                    break
                
        #print('test1')
        #print(useful)
        #print(pos_1_char,pos_2_char)
        #print()
        
        char_1 = useful['m1'][pos_1_char]
        cipher_char_1 = useful['c1'][pos_1_char]
        key_increment = (ord(useful['c1'][pos_2_char])
                        - ord(useful['c1'][pos_1_char])) % 26

        #print('test2')
        #print(char_1, cipher_char_1, key_increment)
        #print()
        
        for i in range(len(useful['m1'])):
            diff = ord(useful['m1'][i]) - ord(char_1)
            if ord(useful['c1'][i]) != ((ord(cipher_char_1) + diff*key_increment) % 26):
                pos_1_char = i
                char_1 = useful['m1'][pos_1_char]
                cipher_char_1 = useful['c1'][pos_1_char]
                break
        
        #print('test3')
        #print(char_1, cipher_char_1)
        #print()
        
        for i in range(26):
            dic.update({chr((ord(cipher_char_1)-97+i*key_increment)%26+97):
                        chr((ord(char_1)+i-97)%26+97)})
            
        for i in range(len(useful['c2'])):
            if ord(useful['c2'][i]) >= 97 and ord(useful['c2'][i]) <= 122:
                useful['m2'] += dic[useful['c2'][i]]
            elif ord(useful['c2'][i]) >= 65 and ord(useful['c2'][i]) <= 90:
                useful['m2'] += (dic[useful['c2'][i].lower()]).upper()
            else:
                useful['m2'] += useful['c2'][i]
        
        print(useful['m2'])
        self.r.sendline(useful['m2'])
        return
    
    def sol_6(self):
        self.p = self.r.recvuntil('m2 = ?\n').decode()
        print(self.p)

        statements = []
        useful = {'m1':'','c1':'','c2':'','m2':''}
        
        statements = self.p.splitlines()
        for comp in statements:
            if comp.find('m1') != -1:
                useful['m1'] = comp[comp.find('=')+2:]
            elif comp.find('c1') != -1:
                useful['c1'] = comp[comp.find('=')+2:]
            elif comp.find('c2') != -1:
                useful['c2'] = comp[comp.find('=')+2:]

        #print(useful)

        dic_m = {}
        dic_c = {}
        for char in useful['m1']:
            if char != ' ':
                if char in dic_m:
                    dic_m[char] += 1
                else:
                    dic_m.update({char:1})
                    
        for char in useful['c1']:
            if char != ' ':
                if char in dic_c:
                    dic_c[char] += 1
                else:
                    dic_c.update({char:1})
        #print(dic_m)
        #print(dic_c)

        interval = 0
        cipher1_l = [ch for ch in useful['c1']]
        #print(cipher_l)
        
        for itv in range(1,len(useful['m1'])+1):
            interval = itv
            for i in range(len(useful['m1'])):
                if cipher1_l[(i*interval)%len(useful['m1'])] != useful['m1'][i]:
                    interval = 0
                    break
            if interval != 0:    
                break

        message2_l = [None]*len(useful['c2'])
        
        for i in range(len(useful['c2'])):
            message2_l[i] = useful['c2'][(i*interval)%len(useful['c2'])]
        for ch in message2_l:
            useful['m2'] += ch

        print(useful['m2'])
        self.r.sendline(useful['m2'])
        return
            
r = remote('cns.csie.org',10200)
ctf = captureFlag(r)
ctf.request()
ctf.sol_1()
ctf.request(2)
ctf.sol_2()
ctf.request(2)
ctf.sol_3()
ctf.request(3)    
ctf.sol_4()
ctf.sol_5()
ctf.sol_6()

flag = ctf.r.recvall().decode()
print(flag)
print()
print(flag[46:79])
import base64
encoded = flag[46:79]
decoded = base64.b64decode(encoded)
print(decoded.decode())
f = open('problem4.txt','w')
f.write(decoded.decode())
f.close()
#ctf.request()
#ctf.request(-1)
#print(ctf.p)

