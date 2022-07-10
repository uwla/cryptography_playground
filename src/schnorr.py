#!/usr/bin/python3
from cripto_utils import bits, concat, exp_mod, factors, prime_gt
from random import randint

p = prime_gt(15000)
q = factors(p-1)[-1][0]
g = randint(2, p)
b = exp_mod(g, int((p-1)/q), p)
t = randint(1, bits(q))

# placeholder/stub for an actual hashing function
def hash(x):
    return exp_mod(x, 7, 1373)

# Alice's key
def schnorr_genkeys():
    s = randint(1, q-1)     # sec key
    v = exp_mod(b, -s, p)   # pub key
    return (v, s)

def schnorr_sign(keys, x):
    v, s = keys
    r = randint(1, q-1)
    u = exp_mod(b, r, p)
    e = hash(concat(x, u))
    y = (s*e + r) % q
    return (y, e)

def schnorr_verify(pkey, x, signature):
    v = pkey
    y, e = signature
    z = (exp_mod(b, y, p) * exp_mod(v, e, p)) % p
    e_ = hash(concat(x, z))
    return e_ == e

def test_schnorr_signature():
    keys = schnorr_genkeys()
    pkey = keys[0]
    x = randint(1, 10000)
    signature = schnorr_sign(keys, x)
    verification = schnorr_verify(pkey, x, signature)
    print(verification, x, signature)

test_schnorr_signature()
