#!/usr/bin/python3
from crypto_utils import exp_mod, prime_gt
from crypto_types import KeyAgreementProtocol
from random import randint

class MTI(KeyAgreementProtocol):
    def generate_public_parameters(self, sec_level):
        p = prime_gt(sec_level)
        g = randint(2, p-1)
        self.public_params = (p, g)

    def generate_key(self):
        p, g = self.get_public_params()
        s = randint(2, p-2)
        t = exp_mod(g, s, p)
        n = randint(2, p-2)
        return (t, (s, n))

    def generate_pub_data(self, key):
        p, g = self.get_public_params()
        t, (s, n) = key
        u = exp_mod(g, n, p)
        return (t, u)

    def agree_shared(self, sender_key, receiver_pub_data):
        p, g = self.get_public_params()
        tB, uB = receiver_pub_data
        tA, (sA, nA) = sender_key
        uA = exp_mod(g, nA, p)
        return (exp_mod(uB, sA, p) * exp_mod(tB, nA, p)) % p

if __name__ == "__main__":
    mti = MTI(10000)
    mti.test_key_agreement()