#!/usr/bin/python3
from cripto_utils import exp_mod, prime_between
from random import randint

p = prime_between(8000, 10000)
g = randint(2, p-1)

sA = randint(2, p-2)    # sec key
tA = exp_mod(g, sA, p)  # pub key
nA = randint(2, p-2)    # nonce
uA = exp_mod(g, nA, p)  # shared key

sB = randint(2, p-2)    # sec key
tB = exp_mod(g, sB, p)  # pub key
nB = randint(2, p-2)    # nonce
uB = exp_mod(g, nB, p)  # shared key

kA = (exp_mod(uB, sA, p) * exp_mod(tB, nA, p)) % p
kB = (exp_mod(uA, sB, p) * exp_mod(tA, nB, p)) % p

if kA != kB:
    raise Exception("something went wrong")

K = kA
print(K)
