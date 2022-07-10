#!/usr/bin/python3
from cripto_utils import exp_mod, prime_between
from random import randint

def gen_key_pair(secmin=1000, secmax=10000):
    p = prime_between(secmin, secmax)
    g = randint(2, p-1)
    s = randint(2, p-2)
    t = exp_mod(g, s, p)
    return ((p, g, t), s)

def send_msg(senderKeys, destPubKey, text):
    (pA, gA, tA), sA = senderKeys
    pB, gB, tB = destPubKey
    uA = exp_mod(gB, sA, pB)
    K = exp_mod(tB, sA, pB)
    cipher = K^text
    return (uA, cipher)

def recv_msg(destKeys, msg_enc):
    (pB, gB, tB), sB = destKeys
    uA, cipher = msg_enc
    K = exp_mod(uA, sB, pB)
    text = K^cipher
    return text

keysA = gen_key_pair()
keysB = gen_key_pair()
pubkeyB = keysB[0]

text = randint(2, 255)
enc = send_msg(keysA, pubkeyB, text)
dec = recv_msg(keysB, enc)
print(text, enc, dec)
