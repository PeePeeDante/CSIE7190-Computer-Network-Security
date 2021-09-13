# Problem Description
## Capture The Flag
### 4. Simple Crypto (10%) <br/>
Welcome to the Crypto World. In this homework, you are going to play with some well known classical ciphers. Please solve all the classical cipher challenges yourself. Even though classical ciphers only used in the past and most of them can be practically computed and solved, I don’t think you can figure it out that easily :P. Be careful and don’t use classical ciphers to keep your secret! <br/>

How to run code: <br/>
1. Run code4.py with python <br/>
2. During runtime, input ‘y’ when the appearing line of text turns meaningful. <br/>
3. Flag will be shown on screen after finishing previous step.<br/>
4. Flag is in problem4.txt.<br/>


### 5. Find The Secret (10%) <br/>
My friends and I built a Shamir’s Secret Sharing scheme using a polynomial A(x) = a0 + a1x + a2x2, where the secret is a0. The ith user receives Di=(i,A(i) modq), where q is a prime. I have collected the secret shares from 1st, 2nd and 3rd users (D1, D2, D3). However, some bad guys forged lots of faked secret shares, trying to prevent us from retrieving our secret. Can you help me find the secret? <br/>
My friend gave me some hints to find out the true secret shares, ci = gai mod p, 0 ≤ i ≤ 2, where p is also a prime and q|(p−1), g ∈ Zp∗ and g is an element of order q. The data is included in hw1/secret_sharing. <br/>

How to run code: <br/>
1. Run code5.py with python <br/>
2. Wait until D1, D2, D3 appears patiently haha. <br/>
3. The a0 secret is in problem5.txt, along with D1, D2, D3. <br/>

### 6. Cute Baby Cat (20%) <br/>
Are you cats lover? There is an organization owns the best cat collection, however, you have to pass through layers of permission control to get them! <br/>
You can access the system by nc cns.csie.org 10202, and the challenge is also included in hw1/cbc. <br/>

How to run code: <br/>
1. Run code6.py with python <br/>
2. Wait until “done”. Then the flag appears <br/>
3. Flag is in problem6.txt. <br/>
4. Only able to solve for one flag. <br/>
