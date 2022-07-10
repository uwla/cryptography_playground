#!/usr/bin/python3
from cripto_utils import exp_mod, factors, mod_inv, prime_gt
from random import randint

def dsa_genkeys(seclevel=12345):
    # public primes
    p = prime_gt(seclevel)
    q = factors(p-1)[-1][0] # pick last factor of p-1


    # generator
    g = 1
    while g == 1:
        h = randint(2, p-2)
        g = exp_mod(h, int((p-1)/q), p)

    # seckey
    s = randint(2, q-1)

    # another pubkey
    t = exp_mod(g, s, p)

    return ((p, q, g, t), s)

def dsa_sign(keys, x):
    (p, q, g, t), s = keys
    k = randint(2, q-1)
    kinv = mod_inv(k, q)
    c = exp_mod(g, k, p) % q
    d = ((x + s*c)*kinv) % q
    return (c, d)

def dsa_verify(pkey, x, signature):
    p, q, g, t = pkey
    c, d = signature
    dinv = mod_inv(d, q)
    e1 = (x*dinv) % q
    e2 = (c*dinv) % q
    a = exp_mod(g, e1, p) * exp_mod(t, e2, p)
    b = ((a%p)%q)
    return b == c

def test_dsa_signature():
    keys = dsa_genkeys()
    pkey = keys[0]
    p = pkey[0]
    x = randint(1,p-1)
    signature = dsa_sign(keys, x)
    verification = dsa_verify(pkey, x, signature)
    print(verification, x, signature)

test_dsa_signature()
