import csv
import numpy as np
from math import sqrt

EbNo = 0.6
p_BEC = 0.5
p_BSC = 0.3


def get_csv():
    csv_file = []
    with open('Mondrian.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file.append([int(float(num)) for num in row])
    return csv_file


def modulate_cword(cword, eb, t):
    #step 1
    b = []
    for i in cword:
        if i == 0: b.append(-1)
        else: b.append(1)
    A = b.copy()

    # step 2
    for i, bi in enumerate(b):
        op = sqrt(abs(bi*eb))
        if bi == -1: A[i] = -op
        else: A[i] = op

    # step 3
    #A = [x * (1/sqrt(t)) for x in A]
    return A


def AWGN_noise(cword_intervals):
    noise_col = np.random.normal(loc=0, scale=EbNo, size=(1, cword_intervals))
    return noise_col.flatten()


# noice = 0 => no noice
# noice = 1 => noice
def BEC_noice(cword):
    if np.random.uniform(0, 1) <= p_BEC:
        return 'e'
    else:
        return cword


def BSC_noice(cword):
    if np.random.uniform(0, 1) <= p_BSC:
        return (0)**cword
    else:
        return cword


bec_image = get_csv()
for i_row, row in enumerate(bec_image):
    for i_col, col in enumerate(row):
        bec_image[i_row][i_col] = BEC_noice(col)


bsc_image = get_csv()
for i_row, row in enumerate(bsc_image):
    for i_col, col in enumerate(row):
        bec_image[i_row][i_col] = BSC_noice(col)


awgn_image = get_csv()
for i_row, row in enumerate(awgn_image):
        signal = modulate_cword(row, EbNo, 1/len(row))
        noise = AWGN_noise(len(row))
        signal = [x+y for x, y in zip(signal, noise)]
        awgn_image[i_row] = signal




