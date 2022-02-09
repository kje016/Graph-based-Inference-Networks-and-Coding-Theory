# cd Desktop/INF244/Exercises/MA2
import numpy as np
from sage.all import *


def vi(matrix):
    v = []
    for row in matrix:
        v.append(max([sum(row[i].degrees()) for i in range(len(row))])-1)
    return v


def iterate_register(mat, input_bit, crnt_state):
    eval = mat.substitute(x0=input_bit, x1=crnt_state[0], x2=crnt_state[1])
    output = list(eval[0])
    next_state = [input_bit] + crnt_state[:len(crnt_state)-1]

    return output, next_state


def zero_force_machine(mat, input_vector):
    v = int(mat.nrows())
    elem = tuple(vector(GF(2), [0]*v))
    pad = [elem]*v
    return (list(input_vector)+pad)


def convolutional_encoder(message, matrix):
    output = []
    pad = max(vi(matrix))
    state = [0]*pad
    sequence = list(message) + [0]*pad
    for mi in sequence:
        oi, state = iterate_register(matrix, mi, state)
        output.extend(oi)
    return np.array(output), state



