# cd Desktop/INF244/Exercises/MA3
from sage.all import *
import csv

import BEC_minsum
import MLdecoder
import Minsum
import Gallager
# Libraries
import numpy as np
import matplotlib as mpl
mpl.use('template')
import matplotlib.pyplot as plt
from scipy.stats import norm


def mat_csv_fun(file):
    output = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            output.append([int(x) for x in row])
        return Matrix(GF(2), output)

G = mat_csv_fun('G.csv')
H = mat_csv_fun('H.csv')
dH = mat_csv_fun('debug_H.csv')

# Parameters
k, n = G.nrows(), G.ncols()
R = k/n     # Rate of the code
lim = 5  # number or errors to be reached before moving to the next SNR value
SNR = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
sigma = np.sqrt(1/(2*R*10**(SNR/10)))
p = 1-norm.cdf(1/sigma)     # error probability, from proposition 2.9
BEgraph = np.zeros((3, len(SNR)))   # Vector containing P_b
np.random.seed(314150304)   # Random seed. Use your own
# C = MLdecoder.gen_cs(G)
C = LinearCode(G)
for i in range(len(SNR)):
    print(SNR[i])
    BE = np.zeros(3)    # Stores the number of errors so far for each decoder
    N0 = 2*sigma[i]**2
    runs = 0
    while np.min(BE)<lim:
        # Monte Carlo Simulation
        runs = runs+1
        m = random_vector(GF(2), k)     # vector(GF(2), (np.random.rand(k)>0.5)*1)
        v = vector(RealField(10), m*G)

        noise = (np.random.normal(0, 0.4, size=len(v)))
        r = (2*v)-vector([1]*len(v))+vector(list(noise))
        r = vector(RealField(10), [-2.2, -2.2, -2.2, 2.2, 2.2, 2.2])
        # print(f"noise := {noise}")
        # Gallager decoding
        mhat, is_codeword = Gallager.spa_main(G=G, H=H, r=r, N0=N0)
        BE[0] = BE[0]+(mhat+m).hamming_weight()
        # MinSum decoding
        mhat, _ = Minsum.spa_main(G=G, H=dH, r=r, N0=N0)
        # mhat, _ = BEC_minsum.minsum_SPA(H=dH, r=r, N0=N0, channel='BEC', sigma=0)
        BE[1] = BE[1]+(mhat+m).hamming_weight()
        # Maximum-likelihood decoding
        mhat = MLdecoder.main(G=G, r=r, all_cs=C)
        # print(mhat, m, BE[2])
        BE[2] = BE[2]+(mhat+m).hamming_weight()
        if runs > 4000:
            break
        # print(BE)
    for j in range(3):
        BEgraph[j, i] = BE[j]/(runs*np.size(m))   # Bit Error Probability
    breakpoint()
    plt.plot(SNR, p)
    plt.plot(SNR, np.transpose(BEgraph))
    plt.yscale('log')
    plt.grid(axis='y')
    plt.legend(['Uncoded BPSK', 'Gallager SPA', 'MinSum', 'ML'])
    plt.xlabel('SNR (dB)')
    plt.ylabel('Pb')
plt.savefig(f'MA3_chart.png')
