#!/usr/bin/python3
from cripto_utils import modinv

def crt(p, r):
    M = 1
    n = len(p)
    for i in range(n):
        M = M * p[i]
    x = 0
    for i in range(n):
        m = M/p[i]
        m_inv = modinv(p[i], m)
        x = (x + m * m_inv * r[i]) % M
    return x
