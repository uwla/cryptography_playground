#!/usr/bin/python3
from cripto_utils import exp_mod, factors, mod_inv, prime_gt
from cripto_types import SignatureScheme
from random import randint

class DSA(SignatureScheme):
    def generate_public_parameters(self, sec_level):
        # generate public primes
        p =  prime_gt(sec_level)
        q = factors(p - 1)[-1][0]  # pick last factor of p-1

        # public generator
        g = 1
        while g == 1:
            h = randint(2, p - 2)
            g = exp_mod(h, int((p - 1) / q), p)

        # set the public parameters
        self.public_params = (p, q, g)

    def generate_secrete_key(self):
        p, q, g = self.get_public_params()
        s = randint(2, q - 1)
        return s
    
    def derive_public_key(self, sec_key):
        p, q, g = self.get_public_params()
        t = exp_mod(g, sec_key, p)
        return t

    def sign(self, msg, sec_key):
        x = msg
        s = sec_key
        p, q, g = self.get_public_params()
        t = self.derive_public_key(s)
        k = randint(2, q - 1)
        k_inv = mod_inv(k, q)
        c = exp_mod(g, k, p) % q
        d = ((x + s * c) * k_inv) % q
        return (c, d)

    def verify(self, msg, pub_key, signature):
        x = msg
        t = pub_key
        p, q, g = self.get_public_params()
        c, d = signature
        d_inv = mod_inv(d, q)
        e1 = (x * d_inv) % q
        e2 = (c * d_inv) % q
        a = exp_mod(g, e1, p) * exp_mod(t, e2, p)
        b = (a % p) % q
        return b == c

if __name__ == "__main__":
    dsa_scheme = DSA(10000)
    dsa_scheme.test_signature()
