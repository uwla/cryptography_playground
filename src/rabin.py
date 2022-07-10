#!/usr/bin/python3
from cripto_utils import prime_between, exp_mod, modinv
from random import randint

# seckey
q, r = 1, 1
while q%4 != 3:
    q = prime_between(300, 600)
while r%4 != 3:
    r = prime_between(300, 600)

# pubkey
n = q*r                      

m = randint(1, n-1)
c = exp_mod(m, 2, n)

qinv = modinv(q, r)
rinv = modinv(r, q)
x2 = exp_mod(c, (q+1)/4, q)
x1 = exp_mod(c, (r+1)/4, r)

m1 = (x1*q*qinv+x2*r*rinv) % n
m2 = n-m1
m3 = (x1*q*qinv-x2*r*rinv) % n
m4 = n-m3

if m not in (m1,m2,m3,m4):
    raise Exception("something went wrong")

print(f"m={m}, (m1,m2,m3,m4) = ({m1}, {m2}, {m3}, {m4})")
