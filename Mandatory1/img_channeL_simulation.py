import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import math
from numpy import random

# Read Image
img = mpimg.imread("UIB_logo.png")

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

p = 0.2     # probability of crossover
EbNo = 0.5
N0 = 1.0

#EbNo = 0.6
p_BEC = 0.5
p_BSC = 0.3


def modulate_cword(cword, eb, t):
    #step 1
    b = []
    for i in cword:
        if i == 0: b.append(-1)
        else: b.append(1)
    A = b.copy()

    # step 2
    for i, bi in enumerate(b):
        op = math.sqrt(abs(bi*eb))
        if bi == -1: A[i] = -op
        else: A[i] = op

    # step 3
    A = [x * (1/math.sqrt(t)) for x in A]
    return A


def signal_noise(cword_intervals):
    noise_col = random.normal(loc=0, scale=N0/2, size=(1, cword_intervals))
    return noise_col.flatten()

# noice = 0 => no noice
# noice = 1 => noice
def BEC_noice(cword):
    rand = np.random.uniform(0, 1)
    if rand <= p_BEC:
        return [0.56, 0.56, 0.56, 1]
    return cword


def BSC_noise(cword):
    rand = np.random.uniform(0, 1)
    if rand <= p_BSC:
        return [i**(-1) for i in cword]
    else:
        return cword



#plt.imshow(img)
#plt.show()
bec_image = img.copy()
bec_image_sngl = []
erasure = 'e'

for i_row, row in enumerate(bec_image):
    for i_col, col in enumerate(row):
        bec_image[i_row, i_col] = BEC_noice(col)

bec_image = rgb2gray(bec_image)
bec_image = plt.imshow(bec_image, cmap= plt.get_cmap('gray'))
plt.savefig('BEC_244.png', bbox_inches='tight', transparent=True, pad_inches=0)
plt.title("BEC image")
plt.show()


awgn_image = img.copy()
for i_row, row in enumerate(img):
    for i_col, col in enumerate(row):
        signal = modulate_cword(col, EbNo, 1/len(col))
        noise = signal_noise(len(col))
        signal = [x+y for x, y in zip(signal, noise)]
        awgn_image[i_row, i_col] = signal
awgn_image = rgb2gray(awgn_image)

awgn_image = plt.imshow(awgn_image, cmap= plt.get_cmap('gray'))
plt.title("AWGN image")
plt.show()

bsc_image = img.copy()
for i_row, row in enumerate(bsc_image):
    for i_col, col in enumerate(row):
        bsc_image[i_row, i_col] = BSC_noise(col)

bsc_image = plt.imshow(bsc_image, cmap= plt.get_cmap('gray'))
plt.title("BSC image")
plt.show()


