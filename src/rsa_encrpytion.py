#!/usr/bin/python3
from crypto_utils import exp_mod, gdc, mod_inv, prime_gt, prime_lt
from crypto_types import EncryptionScheme
from random import randint

class RSA(EncryptionScheme):
    def encrypt(self, msg, pub_key):
        p, n = pub_key
        x = msg
        if x >= n:
            raise Exception("Message cannot be greater than pubkey")
        return exp_mod(x, p, n)

    def decrypt(self, msg, sec_key):
        s, n, phi_n = sec_key
        x = msg
        if x >= n:
            raise Exception("Message cannot be greater than pubkey")
        return exp_mod(x, s, n)

    def generate_secrete_key(self):
        q = prime_gt(self.sec_level)
        r = prime_lt(self.sec_level)
        n = q*r
        phi_n = (q-1)*(r-1)
        s = randint(2, phi_n)
        while gdc(s, phi_n) != 1:
            s = randint(2, phi_n)
        return (s, n, phi_n)
    
    def derive_public_key(self, sec_key):
        s, n, phi_n = sec_key
        p = mod_inv(s, phi_n)
        return (p, n)

if __name__ == "__main__":
    rsa_scheme = RSA(1000)
    rsa_scheme.test_encryption()
