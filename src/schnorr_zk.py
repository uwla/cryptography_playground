#!/usr/bin/python3
from cripto_utils import bits, exp_mod, factors, mod_inv, prime_gt, rand_inv
from random import randint

p = prime_gt(15000)
q = factors(p-1)[-1][0]
g = randint(2, p)
b = exp_mod(g, int((p-1)/q), p)
t = randint(1, bits(q))

# Alice's key
s = randint(1, q-1)     # sec key
v = exp_mod(b, -s, p)   # pub key

# Alice -> Bob: x
r = randint(1, q-1)
x = exp_mod(b, r, p)

# Bob -> Alice: e
e = randint(1, 1<<t)

# Alice -> Bob
y = (s*e + r)%q

# verification
z = (exp_mod(b, y, p) * exp_mod(v, e, p)) %p
print(x == z, x, z)
