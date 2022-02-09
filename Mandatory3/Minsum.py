# cd Desktop/INF244/Exercises/MA3
from sage.all import *


def min_update_row(row, min_vals, signs, H_row):
    output, min_get = [0]*len(row), len(min_vals)
    for i, elem in enumerate(H_row.nonzero_positions()):
        if min_vals[-min_get] == abs(row[elem]):
            output[elem] = min_vals[min_get-1]*signs[i]
        else:
            output[elem] = min_vals[-min_get]*signs[i]
    return output


def sum_approx(Lv, min_vals, H):
    output = []
    for i, row in enumerate(Lv):
        sign = (-1)**(len(H[i].nonzero_positions()))
        signs = [-1 if row[pos] < 0 else 1 for pos in H[i].nonzero_positions()]
        P = product(signs)
        Lvi_signs = list([a*b for a, b in zip(signs, [P*sign]*len(signs))])
        Lvi = min_update_row(row, min_vals[i], Lvi_signs, H.row(i))
        output.append(Lvi)
    return Matrix(output)


def min_fun(Lc, n_mins):
    mins = []
    for i, row in enumerate(Lc):
        non_zeros = list(map(lambda a: abs(row[a]), row.nonzero_positions()))
        minis = sorted(non_zeros[:n_mins])
        for j in range(n_mins, len(non_zeros)):
            if non_zeros[j] < minis[-1]:
                minis[-1] = non_zeros[j]
                minis.sort()
        mins.append(minis)
    return mins


def minsum_SPA(r, H, N0):
    # Lj = [1*r[j]for j in range(len(r))] # (4*sqrt(Ec)/N0)*r[j] = 1*r[j] = r[:] in this case
    Lj = r[:]
    Lv = [RealNumber(elem)*Lj[j] for i in range(H.nrows()) for j, elem in enumerate(H.row(i))]
    Lv = Matrix(RealField(10), H.nrows(), H.ncols(), Lv)
    codeword, runs = False, 0
    while not codeword and runs < 20:
        min_vals = min_fun(Lv, 2)
        Lc = sum_approx(Lv=Lv, min_vals=min_vals, H=H)
        l_tot = vector(RealField(10), [sum(Lc.column(i))+r[i] for i in range(len(r))])
        v_hat = vector(GF(2), [0 if elem <= 0 else 1 for elem in l_tot])
        print(v_hat)
        runs += 1

        # check if v_hat is a valid codeword
        if H * v_hat == 0:
            return v_hat, True

        # update Lv
        for j in range(Lc.ncols()):
            pos = H.column(j).nonzero_positions()
            col = [Lc[i, j] for i in pos]
            for i in range(len(col)):
                belief = sum(col[:i] + col[i + 1:])
                Lv[pos[i], j] = belief + Lj[j]
    return v_hat, codeword


def spa_main(G, H, r, N0):
    # RDF = RealDoubleField(), the elements are of double precision floating numbers
    v_hat, is_codeword = minsum_SPA(r, H, N0)
    #m_hat = vector(GF(2), list(v_hat)[:G.nrows()])
    m_hat = v_hat
    return m_hat, is_codeword


#H = Matrix(GF(2), [[1, 0, 1, 0, 1, 0, 1],[0, 1, 1, 0, 0, 0, 1], [1, 1, 0, 1, 0, 1, 0]])
#r = vector(RealField(10), [-0.7, -2.7, -1.5, 0.2, -1.6, -0.8, 0.9])
#minsum_SPA(r, H)

