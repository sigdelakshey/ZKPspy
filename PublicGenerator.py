from sympy import isprime, randprime
import random

from Utils import generate_random, generate_random_bit

class PublicGenerator:
    def __init__(self, bit_length_q=256):
        self.bit_length_q = bit_length_q 
        self.q = self.generate_prime(self.bit_length_q)
        self.p = self.q * 2 + 1 

        while not isprime(self.p):
            self.q = self.generate_prime(self.bit_length_q)
            self.p = self.q * 2 + 1

        self.g = self.find_generator(self.p, self.q, generate_random(self.p))
        self.h = self.find_generator(self.p, self.q, generate_random(self.p))
        self.x = self.generate_private_key(self.bit_length_q) 
        self.y = pow(self.g, self.x, self.p) 

    def generate_prime(self, bit_length):
        return randprime(2**(bit_length-1), 2**bit_length)

    def find_generator(self, p, q, v):
        h = v
        g = pow(h, (p - 1) // q, p)
        while g == 1:
            h += 1
            g = pow(h, (p - 1) // q, p)
        return g

    def generate_private_key(self, bit_length):
        return generate_random_bit(bit_length)

    def display_parameters(self):
        print(f'p: {self.p}')
        print(f'q: {self.q}')
        print(f'g: {self.g}')
        print(f'h: {self.h}')
        print(f'x: {self.x}')
        print(f'y: {self.y}')

if __name__ == "__main__":
    generator = PublicGenerator()
