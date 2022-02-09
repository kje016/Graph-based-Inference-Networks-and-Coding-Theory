# cd Desktop/INF244/Exercises/MA2
from sage.all import *
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from scipy.stats import norm

import Convolutional_Encoder
import Viterbi

x_vars = 3
P = PolynomialRing(GF(2), x_vars, var('x'))
P.inject_variables()
#G = Matrix(P, [x0+x1+x2, x0+x2])
G = Matrix(P, [[x0+x1+x2, x0+x1, x0+x1], [x0, x1, x0+x1]])

R = G.nrows()/G.ncols()          # rate of the code
#encoder_list = G
inf_len = 50      # length of the information sequences
lim = 100   # number or errors to be reached before moving to the next SNR value
SNR = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
sigma = np.sqrt(1/(2*R*10**(SNR/10)))
p = 1 - norm.cdf(1/sigma)       # error probability, from proposition 2.9

BEgraph = np.zeros(len(SNR))    #Vector containing P_b in decoding

np.random.seed(31415) #Random seed. Use your own
for i in range(len(SNR)):
    BE, runs = 0, 0
    while BE < lim:
        runs += 1
        m = (np.random.rand(G.nrows(), inf_len) > 0.5)*1
        c, last_state = Convolutional_Encoder.convolutional_encoder(m[0], G)
        noise = (np.random.rand(len(c)) < p[i])*1
        r = [a+b for a, b in list(zip(c, noise))]
        m_hat = np.array(Viterbi.main_viterbi(G, r, last_state))
        m = np.append(m, np.array(last_state))
        BE = BE+np.sum((m_hat+m)%2)
        if runs > 100000:
            break
        BEgraph[i] = BE/(runs*np.size(m))
        plt.plot(SNR, p)
    plt.plot(SNR, BEgraph)
    plt.yscale('log')
    plt.grid(axis='y')
    plt.legend(['Hard CC'])
    plt.xlabel('SNR (dB)')
    plt.ylabel('Pb')
plt.savefig(f'mychart_G.png')







