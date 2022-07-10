from cripto_utils import concat, exp_mod, prime_between, rand_inv
from random import randint
from hashlib import sha256

p = prime_between(7500, 9000)
q = prime_between(7500, 9000)
n = p*q

k = 10
t = 20

def hash(string):
    return int.from_bytes(sha256(string.encode()).digest(), byteorder='little')

def ffs_genkeys():
    s = []  # seckey
    v = []  # pubkey
    for _ in range(k):
        sj = rand_inv(n)
        s.append(sj)
        v.append(exp_mod(sj, -2, n))
    return (v, s)

def ffs_sign(keys, msg):
    s = keys[1]
    r = []
    x = []
    for _ in range(t):
        ri = randint(1, n-1)
        r.append(ri)
        x.append(exp_mod(ri, 2, n))

    m = str(msg)
    for xi in x:
        m += str(xi)
    h0 = hash(m)

    e = []
    for _ in range(t):
        ei = []
        for __ in range(k):
            eij = h0 & 1
            ei.append(eij)
            h0 = h0>>1
        e.append(ei)
    y = []
    for i in range(t):
        yi = r[i]
        for j in range(k):
            if e[i][j] == 1:
                yi = (yi * s[j]) % n
        y.append(yi)
    return (y, e)

def ffs_verify(pkey, msg, signature):
    v = pkey
    y, e = signature
    z = []
    for i in range(t):
        zi = (y[i]**2) % n
        for j in range(k):
            if e[i][j] == 1:
                zi = (zi * v[j]) % n
        z.append(zi)

    m = str(msg)
    for zi in z:
        m += str(zi)
    h1 = hash(m)

    for i in range(t):
        for j in range(k):
            if e[i][j] != (h1 & 1):
                return False
            h1 = h1>>1
    return True

def test_ffs_signature():
    keys = ffs_genkeys()
    pkey = keys[0]
    x = randint(1, 100000)
    signature = ffs_sign(keys, x)
    verification = ffs_verify(pkey, x, signature)
    print(verification, x)
    ## uncomment below to see pretty ugly output
    # print(signature)

test_ffs_signature()
