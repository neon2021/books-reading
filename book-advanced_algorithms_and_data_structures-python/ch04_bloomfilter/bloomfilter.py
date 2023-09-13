import random
import math
from math import log as ln
# import numpy as np 
# from numpy import log as ln 

# jaybaird/python-blooom begin
import hashlib
import bitarray
# jaybaird/python-blooom end

# from ChatGPT begin
import sys
# from ChatGPT end

# I am stuck at here 2023_09_13_WED, completing an eligible bloom filter implementation
#  needs to master the principles of various hash algorithms,
#  such as Murmur hashing and Fowler-NollVo hashing
#
# refer to: https://peps.python.org/pep-0456/
# def fnv(p):
#     if len(p) == 0:
#         return 0
    
#     # bit mask, 2**32-1 or 2**64-1
#     mask = 2 * sys.maxsize + 1

#     x = hashsecret.prefix



class BloomFilter:
    maxS = 10000
    BITS_PER_INT=sys.int_info.bits_per_digit

    def __init__(self, maxSize:int, maxTolerance=0.01, seed=None):
        if seed is None:
            self.seed = random.random()
        self.size = 0
        self.maxSize = maxSize
        # num_bits(in jaybaird) == self.numBits
        # self.numBits = -math.ceil(maxS * ln(maxTolerance) / ln(2) / ln(2) )
        self.numBits = -math.ceil(self.maxSize * ln(maxTolerance) / ln(2) / ln(2) )
        if numBits > MAX_SIZE:
            raise Exception('Overflow')
        # num_slices(in jaybaird) == self.numHashFunctions
        self.numHashFunctions = math.ceil(ln(maxTolerance) / ln(2))
        numElements = math.ceil(numBits / BITS_PER_INT)
        self.bitsArray = bitarray.bitarray(self.numBits, endian='little')
        self.bitsArray.setall(0)
        self.hashFunctions = initHashFunctions(self.numHashFunctions, self.maxSize)
        pass

    def contains(self, key, positions=None):
        if positions is None:
            positions = key2positions(self.hashFunctions)
        return all(map(lambda i : self.readBit(self.bitsArray, i)!=0, positions))

    def insert(self, key):
        positions = key2positions(key)
        if not self.contains(key, positions):
            self.size = self.size + 1
            map(lambda i : writeBit(self.bitsArray, i), positions)