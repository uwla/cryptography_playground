from cripto_utils import concat, exp_mod, prime_gt, prime_lt, rand_inv, randint
from cripto_types import SignatureScheme
from hashlib import sha256

class FeigeFiatShamir(SignatureScheme):
    def generate_public_parameters(self, sec_level):
        p = prime_gt(sec_level)
        q = prime_lt(sec_level)
        n = p*q
        k = 10
        t = 20
        self.public_params = (n, k, t)

    def hash(self, string):
        return int.from_bytes(sha256(string.encode()).digest(), byteorder='little')

    def generate_secrete_key(self):
        s = []
        n, k, t = self.get_public_params()
        for _ in range(k):
            si = rand_inv(n)
            s.append(si)
        return s
    
    def derive_public_key(self, sec_key):
        v = []
        s = sec_key
        n = self.get_public_params()[0]
        for sj in s:
            v.append(exp_mod(sj, -2, n))
        return v

    def sign(self, msg, sec_key):
        pub_key = self.derive_public_key(sec_key)
        s = sec_key
        v = pub_key
        r = []
        x = []
        n, k, t = self.get_public_params()

        for _ in range(t):
            ri = randint(1, n-1)
            r.append(ri)
            x.append(exp_mod(ri, 2, n))

        m = str(msg)
        for xi in x:
            m += str(xi)
        h0 = self.hash(m)

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

    def verify(self, msg, pub_key, signature):
        v = pub_key
        n, k, t = self.get_public_params()
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
        h1 = self.hash(m)

        for i in range(t):
            for j in range(k):
                if e[i][j] != (h1 & 1):
                    return False
                h1 = h1>>1

        return True

if __name__ == "__main__":
    feige_fiat_shamir_scheme = FeigeFiatShamir(10000)
    feige_fiat_shamir_scheme.test_signature()
