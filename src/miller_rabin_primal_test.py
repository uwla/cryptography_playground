#!/usr/bin/python3
from cripto_utils import exp_mod
from random import randint, seed


def primal_test(n, k):
    t = 0
    aux = n-1
    while (aux > 0) and (aux & 1 == 0):
        t = t+1
        aux = aux>>1
    c = int((n-1)/(1<<t))
    print(f"c={c} t={t}")
    for _ in range(k):
        a = randint(2, n-1)
        d = exp_mod(a, c, n)
        print(f"a={a}, d={d}, n={n}")
        rprev = d
        for __ in range(t):
            r = rprev**2 % n
            if r == 1 and (1 != rprev != n-1):
                return False
            rprev = r
        if rprev != 1:
            return False
    return True

