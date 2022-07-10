#!/usr/bin/python3
from cripto_utils import concat, crt, exp_mod, mod_inv, prime_gt, prime_lt, rand_inv
from random import randint

# placeholder/stub for an actual hashing function
def hash(x):
    return exp_mod(x, 7, 1373)

def gq_genkeys(seclevel=1000):
    p = prime_gt(seclevel)
    q = prime_lt(seclevel)
    n = p*q
    phi_n = (p-1)*(q-1)
    j = rand_inv(n)
    e = rand_inv(phi_n)
    jinv = mod_inv(j, n)
    d1 = mod_inv(e, p-1)
    d2 = mod_inv(e, q-1)
    s1 = exp_mod(jinv, d1, p)
    s2 = exp_mod(jinv, d2, q)
    s = int(crt([p, q], [s1, s2]))
    return ((n, e, j), s)

def gq_sign(keys, x):
    (n, e, j), s = keys
    k = randint(1, 10000)
    r = exp_mod(k, e, n)
    t = hash(concat(x, r))
    a = (k*exp_mod(s, t, n)) % n
    return (a, t)

def gq_verify(pkey, x, signature):
    n, e, j = pkey
    a, t = signature
    u = exp_mod(a, e, n) * exp_mod(j, t, n) % n
    t_ = hash(concat(x, u))
    return t == t_

def test_gq_signature():
    keys = gq_genkeys()
    pkey = keys[0]
    p = pkey[0]
    x = randint(1,p-1)
    signature = gq_sign(keys, x)
    verification = gq_verify(pkey, x, signature)
    print(verification, x, signature)

test_gq_signature()
