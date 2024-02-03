#!/usr/bin/python3
from cripto_utils import bits, concat, exp_mod, factors, prime_gt
from cripto_types import SignatureScheme
from random import randint

class Schnorr(SignatureScheme):
    def generate_public_parameters(self, sec_level):
        p = prime_gt(sec_level)
        q = factors(p-1)[-1][0]
        g = randint(2, p-1)
        b = exp_mod(g, int((p-1)/q), p)
        t = randint(1, bits(q))       
        self.public_params = (p, q, g, b, t)

    # placeholder/stub for an actual hashing function
    def hash(self, x):
        return exp_mod(x, 7, 1373)

    def generate_secrete_key(self):
        q = self.get_public_params()[1]
        s = randint(1, q-1)
        return s
    
    def derive_public_key(self, sec_key):
        s = sec_key
        p, q, g, b, t = self.get_public_params()
        v = exp_mod(b, -s, p)
        return v

    def sign(self, msg, sec_key):
        x = msg
        s = sec_key
        v = self.derive_public_key(s)
        p, q, g, b, t = self.get_public_params()

        r = randint(1, q-1)
        u = exp_mod(b, r, p)
        e = self.hash(concat(x, u))
        y = (s*e + r) % q
        return (y, e)

    def verify(self, msg, pub_key, signature):
        x = msg
        v = pub_key
        y, e = signature
        p, q, g, b, t = self.get_public_params()

        z = (exp_mod(b, y, p) * exp_mod(v, e, p)) % p
        h = self.hash(concat(x, z))
        return h == e
        
if __name__ == "__main__":
    schnorr_scheme = Schnorr(10000)
    schnorr_scheme.test_signature()