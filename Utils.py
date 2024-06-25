from hashlib import sha256
import random

def generate_random(p):
    return random.randint(0, p - 1)

def generate_random_bit(bit_length):
    return random.SystemRandom().getrandbits(bit_length)

def hash(value, p):
    value_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    hashed = int.from_bytes(sha256(value_bytes).digest(), byteorder='big')
    return hashed % (p - 1)

def hash(value1, value2, p):
    digest = sha256()
    digest.update(value1.to_bytes((value1.bit_length() + 7) // 8, byteorder='big'))
    digest.update(value2.to_bytes((value2.bit_length() + 7) // 8, byteorder='big'))
    return int.from_bytes(digest.digest(), byteorder='big') % (p - 1)

