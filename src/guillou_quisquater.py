#!/usr/bin/python3
from crypto_utils import concat, crt, exp_mod, mod_inv, prime_gt, prime_lt, rand_inv
from crypto_types import SignatureScheme
from random import randint

class GuillouQuisquater(SignatureScheme):
    # Mocking an actual hashing function.
    # For learning purposes, it does not matter too much the implementation of the hashing.
    def hash(self, x):
        return exp_mod(x, 7, 1373)

    def generate_secrete_key(self):
        p = prime_gt(self.sec_level)
        q = prime_lt(self.sec_level)
        n = p*q
        phi_n = (p-1)*(q-1)
        j = rand_inv(n)
        e = rand_inv(phi_n)
        j_inv = mod_inv(j, n)
        d1 = mod_inv(e, p-1)
        d2 = mod_inv(e, q-1)
        s1 = exp_mod(j_inv, d1, p)
        s2 = exp_mod(j_inv, d2, q)
        s = int(crt([p, q], [s1, s2]))
        pub_key = (n, e, j)
        return (s, pub_key)
    
    def derive_public_key(self, sec_key):
        s, pub_key = sec_key
        return pub_key
    
    def sign(self, msg, sec_key):
        x = msg
        s, (n, e, j) = sec_key
        k = randint(1, 10000)
        r = exp_mod(k, e, n)
        t = self.hash(concat(x, r))
        a = (k*exp_mod(s, t, n)) % n
        return (a, t)

    def verify(self, msg, pub_key, signature):
        x = msg
        n, e, j = pub_key
        a, t = signature
        u = exp_mod(a, e, n) * exp_mod(j, t, n) % n
        h = self.hash(concat(x, u))
        return t == h

if __name__ == "__main__":
    guillou_quisquater_scheme = GuillouQuisquater(10000)
    guillou_quisquater_scheme.test_signature()
