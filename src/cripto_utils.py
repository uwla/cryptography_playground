#!/usr/bin/python3
from random import randint

def gdc(a, b):
    if b > a:
        a, b = b, a
    r = a % b
    if r == 0:
        return b
    return gdc(b, r)

def modinv(n, m):
    if n > m:
        n = n % m
    if gdc(n, m) != 1:
        raise Exception(f"{n} and {m} aren't coprimes!")
    r2, x2, y2 = m, 1, 0
    r1, x1, y1 = n, 0, 1
    while True:
        r = r2%r1
        q = int((r2 - r)/r1)
        x = x2-q*x1
        y = y2-q*y1
        if r == 1:
            return (y+m) % m
        r2, x2, y2 = r1, x1, y1
        r1, x1, y1 = r, x, y

def rand_inv(n):
    k = randint(2, n)
    while gdc(k, n) != 1:
        k = randint(2, n)
    return k

def exp(m, e):
    if e == 0:
        return 1
    if e % 2 == 1:
        return m * exp(m, (e-1)/2)**2
    else:
        return exp(m, e/2) ** 2

def exp_mod(m, e, n):
    if e == 0:
        return 1
    if e % 2 == 1:
        return (m * exp_mod(m, (e-1)/2, n)**2) % n
    else:
        return (exp_mod(m, e/2, n) ** 2) % n

def binary_search(array, x):
    start = 0
    end = len(array) - 1
    while end - start > 1:
        middle = (start+end)>>1
        if array[middle] <= x:
            start = middle
        else:
            end = middle
    if array[end] <= x:
        return end
    else:
        return start

primes = [2, 3]
def is_prime(x):
    for prime in primes:
        if x == prime:
            return True
        if x % prime == 0:
            return False
    return True

def gen_primes_untill(n):
    last_prime = primes[-1]
    nextn = last_prime + 2
    while nextn <= n:
        if is_prime(nextn):
            primes.append(nextn)
        nextn += 2

def prime_gt(x):
    gen_primes_untill(x)
    ind = binary_search(primes, x)
    return primes[ind]

def prime_lt(x):
    gen_primes_untill(x)
    ind = binary_search(primes, x)
    return primes[ind-1]

def prime_between(a, b):
    if a>b:
        raise Exception("invalid range")
    gen_primes_untill(b)
    indA = binary_search(primes, a)
    indB = binary_search(primes, b)
    ind = randint(indA, indB)
    return primes[ind]

def factors(x):
    sqrtx = int(0.5+x**(0.5))
    gen_primes_untill(sqrtx)
    f = []
    for p in primes:
        if p > sqrtx:
            break
        e = 0
        while x%p == 0:
            x = int(x/p)
            e = e+1
        if e != 0:
            f.append([p, e])
    if x != 1:
        f.append([x, 1])
    return f
