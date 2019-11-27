from ntru.Poly import PolyRingModP, DTYPE
from ntru.KeyGen import PubKey, PARAMETER_SETS

import numpy as np

class Manager:

    def __init__(self, parameter):
        self.key = PubKey(parameter)

    def encrypt(self, binary_bits):
        if type(binary_bits) is np.ndarray:
            self.msg_size = binary_bits.size
            m = np.pad(binary_bits, (0, max(0, self.key.N-binary_bits.size)))
            return self.key.R.coefs + m
        else:
            NotImplemented

    def decrypt(self, e):
        if type(e) is np.ndarray:
            A = PolyRingModP.mul(self.key.N, e, self.key.f.coefs) % self.key.q
            A = PolyRingModP.centralized(A, self.key.q)
            return (A % self.key.p)[:self.msg_size]

if __name__ == '__main__':
    test = Manager(PARAMETER_SETS.get("ees743ep1"))
    msg = np.array([1, 0, 1, 0, 1, 0], dtype=DTYPE)
    e = test.encrypt(msg)
    print(test.decrypt(e))
