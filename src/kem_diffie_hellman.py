#!/usr/bin/python3
from crypto_utils import exp_mod, prime_gt
from crypto_types import KeyAgreementProtocol
from random import randint

class DiffieHellman(KeyAgreementProtocol):
    def generate_public_parameters(self, sec_level):
        p = prime_gt(sec_level)
        g = randint(2, p-1)
        self.public_params = (p, g)

    def generate_key(self):
        p, g = self.get_public_params()
        s = randint(2, p-2)
        t = exp_mod(g, s, p)
        return (t, s)

    def generate_pub_data(self, key):
        pub_key, sec_key = key
        return pub_key

    def agree_shared(self, sender_key, receiver_pub_data):
        p = self.get_public_params()[0]
        s = sender_key[1]
        t = receiver_pub_data
        return exp_mod(t, s, p)

if __name__ == "__main__":
    diffie_hellman = DiffieHellman(10000)
    diffie_hellman.test_key_agreement()