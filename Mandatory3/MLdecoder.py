# cd Desktop/INF244/Exercises/MA3
from sage.all import *


def gen_cs(mat):
    output = []
    for i in range(0, 2**(mat.nrows())):
        vec = "{0:b}".format(i)
        vec = "0" * (mat.nrows()-len(vec)) + vec
        vec = vector(GF(2), [int(x) for x in vec])
        output.append(vec*mat)
    return output


def main(G, r, all_cs):
    max_euc = [1 if elem ==1 else -1 for elem in all_cs[0]]
    max_euc = sum([(max_euc[i]-r[i])**2 for i in range(len(r))])
    output = all_cs[0]
    for i in range(1, len(all_cs)):
        c_mod = [1 if elem == 1 else -1 for elem in all_cs[i]]
        euc_d = sum([(c_mod[i]-r[i])**2 for i in range(len(r))])
        if euc_d < max_euc:
            max_euc = euc_d
            output = all_cs[i]
    return vector(GF(2), list(output)[:G.nrows()])

