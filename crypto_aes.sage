#!/bin/sage

#          ╭──────────────────────────────────────────────────────────╮
#          │ GENERAL POLYNOMIAL UTILS                                 │
#          ╰──────────────────────────────────────────────────────────╯

def division(dividend, divisor):
    q,r = dividend.maxima_methods().divide(divisor)
    return q,r

def generate_polynomial(coeff):
    coeff.reverse()
    p=0
    for i in range(0, len(coeff)):
        p+=coeff[i]*x^i
    return p

#          ╭──────────────────────────────────────────────────────────╮
#          │ POLYNOMIAL CONVERSION UTILS                              │
#          ╰──────────────────────────────────────────────────────────╯

def polynomial_to_decimal(p):
    F = GF(2^8)
    P = F['x']
    l = P(p).list()
    d = 0
    for i in range(0,len(l)):
        if l[i] == 1:
            d += 2**i
    return d

def polynomial_to_binary(p):
    b = bin(polynomial_to_decimal(p))
    b = b.replace("0b","")
    return b

def polynomial_to_hexadecimal(p):
    h = hex(polynomial_to_decimal(p))
    h = h.replace("0x","")
    return h

def hex_4bytes_to_polynomial(h):
    a3=int(h[0:2],16)
    a2=int(h[2:4],16)
    a1=int(h[4:6],16)
    a0=int(h[6:8],16)
    return generate_polynomial([a3,a2,a1,a0])

def bin_to_polynomial(b):
    b = b.replace("0b","")
    c = [int(d) for d in list(b)]
    return generate_polynomial(c)

def hex_to_polynomial(h):
    b = bin(int(h,16))
    return bin_to_polynomial(b)

#          ╭──────────────────────────────────────────────────────────╮
#          │ AES UTILS                                                │
#          ╰──────────────────────────────────────────────────────────╯

def aes_subbytes(b1,b2):
    F = GF(2^8,'a')
    R = F['x']
    m = R(x^8+x^4+x^3+x+1)
    p1 = hex_to_polynomial(b1)
    p2 = hex_to_polynomial(b2)
    p = R(p1*p2)
    return p.mod(m)

def aes_mix_column_vectors(ha,hb):
    a3=ha[0:2]
    a2=ha[2:4]
    a1=ha[4:6]
    a0=ha[6:8]
    b3=hb[0:2]
    b2=hb[2:4]
    b1=hb[4:6]
    b0=hb[6:8]
    a0b0 = polynomial_to_decimal(aes_subbytes(a0,b0))
    a0b1 = polynomial_to_decimal(aes_subbytes(a0,b1))
    a0b2 = polynomial_to_decimal(aes_subbytes(a0,b2))
    a0b3 = polynomial_to_decimal(aes_subbytes(a0,b3))
    a1b0 = polynomial_to_decimal(aes_subbytes(a1,b0))
    a1b1 = polynomial_to_decimal(aes_subbytes(a1,b1))
    a1b2 = polynomial_to_decimal(aes_subbytes(a1,b2))
    a1b3 = polynomial_to_decimal(aes_subbytes(a1,b3))
    a2b0 = polynomial_to_decimal(aes_subbytes(a2,b0))
    a2b1 = polynomial_to_decimal(aes_subbytes(a2,b1))
    a2b2 = polynomial_to_decimal(aes_subbytes(a2,b2))
    a2b3 = polynomial_to_decimal(aes_subbytes(a2,b3))
    a3b0 = polynomial_to_decimal(aes_subbytes(a3,b0))
    a3b1 = polynomial_to_decimal(aes_subbytes(a3,b1))
    a3b2 = polynomial_to_decimal(aes_subbytes(a3,b2))
    a3b3 = polynomial_to_decimal(aes_subbytes(a3,b3))
    c6 = a3b3
    c5 = a3b2^^a2b3
    c4 = a3b1^^a2b2^^a1b3
    c3 = a3b0^^a2b1^^a1b2^^a0b3
    c2 = a2b0^^a1b1^^a0b2
    c1 = a1b0^^a0b1
    c0 = a0b0
    C = generate_polynomial([c6,c5,c4,c3,c2,c1,c0])
    r3 =a0b3^^a1b2^^a2b1^^a3b0
    r2 =a0b2^^a1b1^^a2b0^^a3b3
    r1 =a0b1^^a1b0^^a2b3^^a3b2
    r0 =a0b0^^a1b3^^a2b2^^a3b1
    R = generate_polynomial([r3,r2,r1,r0])
    return C,R

#          ╭──────────────────────────────────────────────────────────╮
#          │ ALIASES                                                  │
#          ╰──────────────────────────────────────────────────────────╯

# general polynomial utils
def div(dividend, divisor):
    return division(dividend, divisor)

def genpon(coeff):
    return generate_polynomial(coeff)

# polynomial conversion
def p2bin(p):
    return polynomial_to_binary(p)

def p2hex(p):
    return polynomial_to_hexadecimal(p)

def bin2p(b):
    return bin_to_polynomial(b)

def hex2p(h):
    return hex_to_polynomial(h)

def h4b2p(h):
    return hex_4bytes_to_polynomial(h)

def h2p(h):
    return hex2p(h)

def b2p(b):
    return bin2p(b)

def p2b(p):
    return p2bin(p)

def p2h(p):
    return p2hex(p)

# aes utils
def subb(b1,b2):
    return aes_subbytes(b1,b2)

def mixcol(ha,hb):
    return aes_mix_column_vectors(ha,hb)
