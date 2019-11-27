from test.timeclock import clock
from numba import jit
import random

@clock
@jit
def test_mod(n):
    a = range(n)
    b = range(n)
    for item1, item2 in zip(a, b):
        (item1 + item2) % n

@clock
@jit
def test_if(n):
    a = range(n)
    b = range(n)
    for item1, item2 in zip(a, b):
        if item1 + item2 >= n:
            item1 + item2 - n
        else:
            item1 + item2


@clock
@jit
def test_bit(n):
    for i in range(n):
        n & 2047


@clock
@jit
def test_directly_mod(n):
    for i in range(n):
        n % 2048

@clock
def test_exchange(n):
    a = b = 1
    for i in range(n):
        a, b = b, a

@clock
def test_exchange_by_bit(n):
    a = b = 3
    for i in range(n):
        a ^= b
        b ^= a
        a ^= b

@clock
def test_div(a):
    for i in range(100000000):
        a // 2
@clock
def test_shift(a):
    for i in range(100000000):
        a << 1

@clock
def gen_random_shuffle(N, d, n):
    for i in range(n):
        a = [0 for i in range(N)]
        for i in range(d):
            a[i] = 1
        for i in range(d, 2*d):
            a[i] = -1
        a = random.shuffle(a)

@clock
def gen_random_fetch(N, d, n):
    for i in range(n):
        index_num = 2 * d
        index = []
        while len(index) <= index_num:
            random_num = random.randint(0, N - 1)
            if random_num not in index:
                index.append(random_num)

if __name__ == '__main__':
    # this function is faster??? i can't believe it
    # test_mod(100000000)
    # test_if(100000000)
    # test_bit(100000000)
    # this function is faster??? wocao
    # test_directly_mod(100000000)
    # test_exchange(100000000)
    # test_exchange_by_bit(100000000)
    # test_div(12)
    # test_shift(12)
    gen_random_fetch(401, 133, 1000)
    gen_random_shuffle(401, 133, 1000)