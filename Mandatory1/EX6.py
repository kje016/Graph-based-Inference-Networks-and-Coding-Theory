# cd Desktop/H21/INF244/Exercises/Mandatory1
from sage.all import *
import csv

x_vars = 3
var('x')
R = PolynomialRing(GF(2), x_vars, x)
R.inject_variables()
G = Matrix(R, [[x0+x1, x1, x0], [x4, x2, x2+x3+x4]])

G = Matrix(R, [[x0+1, x0, 1], [x1, 1, 1+x0+x1]])
comlexity = 2 # The length of the longest "lfsr"

G = Matrix(R, [[x0+x1+x2, x0+x1, x0+x2], [x0, x1, x0+x1]])

def vi(matrix):
    v = []
    for row in matrix:
        v.append(max([sum(row[i].degrees()) for i in range(len(row))])-1)
    return v

con_len = vi(G)


def get_csv():
    csv_file = []
    with open('Sequence.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file.append([int(float(num)) for num in row])
    return csv_file


def ex1(input_bit, crnt_state):
    eval = G.substitute(x0=input_bit[0], x1=crnt_state[0][0], x2=input_bit[1], x3=crnt_state[1][0], x4=crnt_state[1][1])
    output = [sum(eval.column(i)) for i in range(eval.ncols())]
    next_state = [[input_bit[i]] + crnt_state[i][:con_len[i]-1] for i in range(G.nrows())]
    #next_state = [input_bit] + crnt_state[:len(crnt_state)-1]
    return output, next_state


def ex2(input_vector):
    v = int(G.nrows())
    elem = tuple(vector(GF(2), [0]*v))
    pad = [elem]*v
    return (list(input_vector)+pad)



def ex3(matrix, message):
    m_pad = ex2(message)
    output = []
    state = [[0]*i for i in vi(matrix)]
    breakpoint()
    for mi in m_pad:
        oi, state = ex1(mi, state)
        output.append(oi)

    return output, state

breakpoint()
sequence = get_csv()
sequence = [a for a in zip(sequence[0], sequence[1])]
ress = ex3(G, sequence)
