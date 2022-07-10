#!/usr/bin/python3
from cripto_utils import exp_mod, factors, mod_inv, prime_between, prime_n, rand_inv
from random import randint

p = prime_between(1000, 1500)
q = prime_between(1000, 1500)
n = p*q
phi_n = (p-1)*(q-1)
v = rand_inv(phi_n)
s = mod_inv(v, phi_n)

# f can be any function but shoud be secure
def f(x):
    return prime_n(x%163)

# CA -> Alice: sA
# CA -> public: iA, jA
iA = randint(2, 1000)               # Alice`s identity
jA = f(iA)                          # Alice`s pubkey
sA = mod_inv(exp_mod(jA, s, n), n)  # Alice`s seckey

# Alice -> Bob: x
r = randint(1, n)     # nonce
x = exp_mod(r, v, n)  # used for ZK proof

# Bob -> Alice: e
e = randint(1, v)     # testimonial

# Alice -> Bob: y
y = (r*exp_mod(sA, e, n)) % n

# verification by Bob
z = (exp_mod(jA, e, n) * exp_mod(y, v, n)) % n
print(z == x, z, x)
