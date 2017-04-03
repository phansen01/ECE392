import itertools
import random

#there are 2^27 possible 3x3x3 matrices, so returning the whole list
#would be a very bad idea. We return a generator instead!
def getTableGenerator():
    possible = [[i for i in itertools.product(range(2), repeat=3)] for _ in range(3)]

    all_3by3 = []

    for i in possible[0]:
        for j in possible[1]:
            for k in possible[2]:
                all_3by3.append(list([i, j, k]))
    
    for matrix_i in all_3by3:
        for matrix_j in all_3by3:
            for matrix_k in all_3by3:
                yield [matrix_i, matrix_j, matrix_k]


