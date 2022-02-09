# cd Desktop/INF244/Exercises/MA3
from sage.all import *


def tanh_fun(Lv, H):
    output = []
    for i, row in enumerate(Lv.rows()):
        row_res = []
        sign = (-1) ** len(row.nonzero_positions()) #(len([elem for elem in row if abs(elem) > 0]))
        row_tanh = list(vector(RealField(10), map(lambda x: tanh(x/2), row)))
        for j in range(len(row)):
            if H[i, j] != 0:
                j_ap = row_tanh[0:j] + row_tanh[j+1:len(row_tanh)]
                j_ap = product([elem for elem in j_ap if abs(elem) > 0])
                row_res.append(sign*2*arctanh(float(j_ap)))
            else:
                row_res.append(0)
        output.append(row_res)
    return Matrix(RealField(10), output)


def comp_l_tot(lc, r):
    return vector([sum(lc.column(i))+r[i] for i in range(len(r))])


def tanh_SPA(r, H, N0):
    #Initialize Lv
    Lj = [((4*1)/N0)*r[j]for j in range(len(r))] # (4*sqrt(Ec)/N0)*r[j] = 1*r[j] = r[:] in this case
    Lv = [RealNumber(elem)*Lj[j] for i in range(H.nrows()) for j, elem in enumerate(H.row(i))]
    Lv = Matrix(RealField(10), H.nrows(), H.ncols(), Lv)

    codeword, runs = False, 0
    while not codeword and runs < 20:
        Lc = tanh_fun(Lv, H)
        l_tot = comp_l_tot(Lc, r)
        v_hat = vector(GF(2), [0 if elem <= 0 else 1 for elem in l_tot])
        runs += 1
        # check if v_hat is a valid codeword
        if H * v_hat == 0:
            return v_hat, True

        #update Lv
        for i, row in enumerate(Lc.rows()):
            for j, col in enumerate(Lc.columns()):
                if H[i, j] != 0:
                    col_res = list(col)[0:i] + list(col)[i + 1:len(col)]
                    Lv[i, j] = Lj[j] + sum(col_res)  # Lj[j]
    return v_hat, codeword


def spa_main(G, H, r, N0):
    # RDF = RealDoubleField(), the elements are of double precision floating numbers
    v_hat, is_codeword = tanh_SPA(r, H, N0)
    m_hat = vector(GF(2), list(v_hat)[:G.nrows()])
    return m_hat, is_codeword
