#!/usr/bin/python
from crypto_utils import exp_mod, mod_inv, prime_gt, rand_inv
from crypto_types import SignatureScheme, EncryptionScheme
from random import randint

class ElGamal(SignatureScheme, EncryptionScheme):
    def generate_public_parameters(self, sec_level):
        p = prime_gt(sec_level)
        g = randint(2, p - 1)
        self.public_params = (p, g)
        

    def generate_secrete_key(self):
        p, g = self.get_public_params()
        s = randint(2, p - 2)  # sec key
        return s
    
    def derive_public_key(self, sec_key):
        p, g = self.get_public_params()
        t = exp_mod(g, sec_key, p)
        return t

    def encrypt(self, msg, pub_key):
        x = msg
        t = pub_key
        p, g = self.get_public_params()
        k = randint(2, p - 1) # nonce
        y = exp_mod(g, k, p)
        z = (exp_mod(t, k, p) * x) % p
        return (y, z)

    def decrypt(self, cipher, sec_key):
        s = sec_key
        t = self.derive_public_key(s)
        p, g = self.get_public_params()
        y, z = cipher
        msg = (z * exp_mod(y, -s, p)) % p
        return msg

    def sign(self, msg, sec_key):
        x = msg
        s = sec_key
        t = self.derive_public_key(s)
        p, g = self.get_public_params()
        k = rand_inv(p - 1)  # nonce
        k_inv = mod_inv(k, p - 1)
        y = exp_mod(g, k, p)
        z = ((x - s * y) * k_inv) % (p - 1)
        return (y, z)

    def verify(self, msg, pub_key, signature):
        x = msg
        t = pub_key
        p, g = self.get_public_params()
        y, z = signature
        a = (exp_mod(t, y, p) * exp_mod(y, z, p)) % p
        b = exp_mod(g, x, p)
        return a == b

if __name__ == "__main__":
    el_gamal_scheme = ElGamal(10000)
    el_gamal_scheme.test_signature()
    el_gamal_scheme.test_encryption()
