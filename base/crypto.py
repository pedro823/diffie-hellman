from base.base_class import BaseClass
from base.error import Error
from random import SystemRandom
random = SystemRandom()

class Crypto(BaseClass):
    """ Class responsible for all random number generation,
        cryptographic encoding and decoding, and """
