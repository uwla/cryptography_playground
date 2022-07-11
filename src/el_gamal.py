#!/usr/bin/python
from cripto_utils import exp_mod, mod_inv, prime_gt, rand_inv
from random import randint

def el_gamal_genkeys(seclevel=4096):
    p = prime_gt(seclevel)  # pub key
    g = randint(2, p-1)     # pub key
    s = randint(2, p-2)     # sec key
    t = exp_mod(g, s, p)    # pub key
    return ((p, g, t), s)

def el_gamal_enc(pkey, x):
    p, g, t = pkey
    k = randint(2, p-1) # nonce
    y = exp_mod(g, k, p)
    z = (exp_mod(t, k, p) * x) % p
    return (y, z)

def el_gamal_dec(keys, enc):
    (p, g, t), s = keys
    y, z = enc
    y_S = exp_mod(y, -s, p)
    x = (z * y_S) % p
    return x

def el_gamal_sign(keys, x):
    (p, g, t), s = keys
    k = rand_inv(p-1) # nonce
    kinv = mod_inv(k, p-1)
    y = exp_mod(g, k, p)
    z = ((x - s*y) *kinv) % (p-1)
    return (y, z)

def el_gamal_verify(pkey, x, signature):
    p, g, t = pkey
    y, z = signature
    a = (exp_mod(t, y, p) * exp_mod(y, z, p)) % p
    b = exp_mod(g, x, p)
    return a == b

def test_el_gamal_encdec():
    keys = el_gamal_genkeys()
    pkey = keys[0]
    p = pkey[0]
    x = randint(1,p-1)
    enc = el_gamal_enc(pkey, x)
    dec = el_gamal_dec(keys, enc)
    print(x==dec, x, enc, dec)

def test_el_gamal_signature():
    keys = el_gamal_genkeys()
    pkey = keys[0]
    p = pkey[0]
    x = randint(1,p-1)
    signature = el_gamal_sign(keys, x)
    verification = el_gamal_verify(pkey, x, signature)
    print(verification, x, signature)

test_el_gamal_encdec()
test_el_gamal_signature()
