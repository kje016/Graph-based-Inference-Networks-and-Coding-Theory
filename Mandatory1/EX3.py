import copy
import csv
from math import floor, ceil, sqrt
from numpy import random
from collections import Counter

EbNo = 0.6
p_BEC = 0.5
p_BSC = 0.3
n_rep = 5
e_symbol = 'e'


def get_csv():
    csv_file = []
    with open('Mondrian.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file.append([int(float(num)) for num in row])
    return csv_file

def count_errors(decoded, original):
    errors = 0
    for i, row in enumerate(decoded):
        for j, col in enumerate(row):
            if decoded[i][j] != original[i][j]:
                errors += 1
            else:
                continue
    return errors

k_seq = get_csv()
n_seq = []
for row in k_seq:
    n_row = []
    for bit in row:
        n_row.extend([bit]*n_rep)
    n_seq.append(n_row)

len_k_seq = sum([len(x) for x in k_seq])


"""         BSC         """
def BSC_noice(cword):
    if random.uniform(0, 1) <= p_BSC:
        return (0)**cword
    else:
        return cword


def rep_decode_BSC(signal):
    B_hat = []
    for row in signal:
        b_row = []
        for i in range(0, len(row), n_rep):
            hw = sum(row[i:i+n_rep])
            if hw <= floor(n_rep/2):
                b_row.append(0)
            elif hw >= ceil(n_rep/2):
                b_row.append(1)
        B_hat.append(b_row)
    return B_hat


bsc_dec = copy.deepcopy(n_seq)
for i_row, row in enumerate(bsc_dec):
    for i_col, col in enumerate(row):
        bsc_dec[i_row][i_col] = BSC_noice(col)

bsc_dec = rep_decode_BSC(bsc_dec)
pe_bsc = count_errors(bsc_dec, k_seq)
print(f"bsc errors := {pe_bsc}, p(error) := {pe_bsc/len_k_seq}")


"""         BEC         """
# noice = 0 => no noice
# noice = 1 => noice
def BEC_noice(cword):
    if random.uniform(0, 1) <= p_BEC:
        return e_symbol
    else:
        return cword


def rep_decode_BEC(signal):
    B_hat = []
    for row in signal:
        b_row = []
        for i in range(0, len(row), n_rep):
            errors = row[i:i+n_rep]
            if 0 in errors:
                b_row.append(0)
            elif 1 in errors:
                b_row.append(1)
            else:
                b_row.append(e_symbol)
        B_hat.append(b_row)
    return B_hat


bec_dec = copy.deepcopy(n_seq)
for i_row, row in enumerate(bec_dec):
    for i_col, col in enumerate(row):
        bec_dec[i_row][i_col] = BEC_noice(col)

bec_dec = rep_decode_BEC(bec_dec)
pe_bec = count_errors(bec_dec, k_seq)
print(f"bec errors := {pe_bec}, p(error) := {pe_bec/len_k_seq}")


"""             AWGN            """
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
    noise_col = random.normal(loc=0, scale=EbNo, size=(1, cword_intervals))
    return noise_col.flatten()

def BSC_decision(rv_list):
    output_list = []
    for a in rv_list:
        if a >= 0: output_list.append(1)
        else: output_list.append(0)
    return output_list

awgn_dec = copy.deepcopy(n_seq)
for i_row, row in enumerate(awgn_dec):
    signal = modulate_cword(row, EbNo, 1/len(row))
    noise = AWGN_noise(len(row))
    awgn_dec[i_row] = [x+y for x, y in zip(signal, noise)]


def rep_decode_AWGN(signal):
    B_hat = []
    for row in signal:
        b_row = []
        for i in range(0, len(row), n_rep):
            hw = sum(BSC_decision(row[i:i+n_rep]))
            if hw <= floor(n_rep / 2):
                b_row.append(0)
            elif hw >= ceil(n_rep / 2):
                b_row.append(1)
        B_hat.append(b_row)
        return B_hat


awgn_dec = rep_decode_AWGN(awgn_dec)
pe_awgn = count_errors(awgn_dec, k_seq)
print(f"awgn errors := {pe_awgn}, p(error) := {pe_awgn/len_k_seq}")
