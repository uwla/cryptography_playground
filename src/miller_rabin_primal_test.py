#!/usr/bin/python3
from crypto_utils import exp_mod, bits
from random import randint
from sys import argv

N = 0
def primal_test(n, k, N):
    t = 0
    aux = n-1
    N+=1
    while (aux > 0) and (aux & 1 == 0):
        t = t+1
        aux = aux>>1
        N += 2
    c = int((n-1)/(1<<t))
    N+=1
    print(f"c={c} t={t}")
    for _ in range(k):
        a = randint(2, n-1)
        d = exp_mod(a, c, n)
        r_prev = d
        N += 2 + bits(c)
        for _ in range(t):
            r = r_prev**2 % n
            if r == 1 and (1 != r_prev != n-1):
                N += 3
                return False, N
            r_prev = r
            N += 4
        N += 1
        if r_prev != 1:
            return False, N
    return True, N

def gen_large_prime(N, min=1123456789, max=9123456789, k=4):
    N = 0
    while True:
        p = randint(min, max)
        isp, N = primal_test(p, k, N)  
        N += 2
        if isp:
            break
    return p, N

if __name__ == "__main__":
    argc = len(argv)
    for i in range(1, argc):
        n = int(argv[i])
        print(primal_test(n, 20, 0)[0])

# print(gen_large_prime(N)[0])
