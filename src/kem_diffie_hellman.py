#!/usr/bin/python3
from cripto_utils import exp_mod, prime_between
from random import randint

p = prime_between(1000, 10000)
g = randint(2, p-1)

sA = randint(2, p-2)
tA = exp_mod(g, sA, p)
sB = randint(2, p-2)
tB = exp_mod(g, sB, p)

kA = exp_mod(tB, sA, p) 
kB = exp_mod(tA, sB, p) 

if kA != kB:
    raise Exception("something went wrong")

kAB = kA
