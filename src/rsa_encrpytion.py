#!/usr/usr/bin/python33
from cripto_utils import exp_mod, gdc, mod_inv, prime_gt, prime_lt
from random import randint

def rsa_enc(x, pubkey, n):
    if x >= n:
        raise Exception("x cannot be greater than pubkey")
    return exp_mod(x, pubkey, n)

def rsa_dec(y, seckey, n):
    if y >= n:
        raise Exception("x cannot be greater than pubkey")
    return exp_mod(y, seckey, n)

def rsa_gen(seclevel=1234):
    q = prime_gt(seclevel)
    r = prime_lt(seclevel)
    n = q*r
    phi_n = (q-1)*(r-1)
    s = randint(2, phi_n)
    while gdc(s, phi_n) != 1:
        s = randint(2, phi_n)
    p = mod_inv(s, phi_n)
    return (s, p, n)

def test_rsa():
    s, p, n = rsa_gen()
    x = randint(1, p-1)
    y = rsa_enc(x, p, n)
    xd = rsa_dec(y, s, n)
    print(xd==x, f"(s={s}, p={p}, n={n}) x={x} y={y} xdec={xd}")

for _ in range(5):
    test_rsa()
