from random import randint
from math import log2

def gdc(a, b):
    if b > a:
        a, b = b, a
    r = a % b
    if r == 0:
        return b
    return gdc(b, r)

def mod_inv(n, m):
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

def rand_inv(n, k_min=2):
    k = randint(k_min, n)
    while gdc(k, n) != 1:
        k = randint(k_min, n)
    return k

def crt(p, r):
    M = 1
    n = len(p)
    for i in range(n):
        M = M * p[i]
    x = 0
    for i in range(n):
        m = int(M/p[i])
        m_inv = mod_inv(m, p[i])
        x = (x + m * m_inv * r[i]) % M
    return x

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
    if e < 0:
        return mod_inv(exp_mod(m, -e, n), n)
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

_primes = [2, 3]
def is_prime(x):
    for prime in _primes:
        if x == prime:
            return True
        if x % prime == 0:
            return False
    return True

def gen_primes_until(n):
    last_prime = _primes[-1]
    next_n = last_prime + 2
    while _primes[-1] < n:
        if is_prime(next_n):
            _primes.append(next_n)
        next_n += 2

def gen_first_primes(n):
    next_n = _primes[-1] + 2
    while len(_primes) < n:
        if is_prime(next_n):
            _primes.append(next_n)
        next_n += 2

def prime_n(n):
    gen_first_primes(n)
    return _primes[n-1]

def prime_gt(x):
    gen_primes_until(x)
    ind = binary_search(_primes, x)
    if _primes[ind] > x:
        return _primes[ind]
    else:
        return _primes[ind+1]

def prime_lt(x):
    if x == 2:
        raise Exception("no prime less than 2")
    gen_primes_until(x)
    ind = binary_search(_primes, x)
    if _primes[ind] < x:
        return _primes[ind]
    else:
        return _primes[ind-1]

def prime_between(a, b):
    if a>b:
        raise Exception("invalid range")
    gen_primes_until(b)
    indA = binary_search(_primes, a)
    indB = binary_search(_primes, b)
    ind = randint(indA, indB)
    return _primes[ind]

def factors(x):
    sqrt_x = int(0.5+x**(0.5))
    gen_primes_until(sqrt_x)
    f = []
    for p in _primes:
        if p > sqrt_x:
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

def bits(x):
    return int(0.5+log2(x))

def concat(a, b):
    return a<<bits(b) + b
