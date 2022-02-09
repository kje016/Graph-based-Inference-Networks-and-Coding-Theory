# cd Desktop/INF244/Exercises/MA2
from sage.all import *
import csv

def get_csv(input_file):
    csv_file = []
    with open(input_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file.extend([int(float(num)) for num in row])
    return csv_file

var('x')
x_vars = 4
R = PolynomialRing(GF(2), x_vars, x)
K = FractionField(R, x)

R.inject_variables()
K.inject_variables()

f1, f2 = x0, x1+x3
G = f1/f2

memory = 3
S, S_pi = [0]*memory, [0]*memory

Pi = get_csv('Permutation.csv')
Pi = [elem-1 for elem in Pi] if not 0 in Pi else Pi # making Pi 0-index if not already

m = get_csv('Sequence.csv')
m_pi = [0]*len(m)
for index, elem in enumerate(Pi):
    m_pi[index] = m[elem]

def run_register(input_bit, state):
    state_input = G.numerator().substitute(x0=input_bit)
    output = state_input + G.denominator().substitute(x1=state[0], x3=state[2])
    next_state = [output]+state[:memory-1]
    return output, next_state


def run_encryption(S, S_pi):
    C = []
    for i, mi in enumerate(m):
        C.append(mi)
        C1, S = run_register(mi, S)
        C2, S_pi = run_register(m_pi[i], S_pi)
        C.extend([C1, C2])
    return C

breakpoint()
C = run_encryption(S, S_pi)
print(f"m_pi = {m_pi}")
print(f"C={C}")
