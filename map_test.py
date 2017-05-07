#!/usr/bin/python3

import matplotlib.pyplot as plt
from noise import noise

def save_image(grid, img_file):
    plt.figure()
    plt.rcParams['figure.figsize'] = [12.,8.]
    plt.imshow(grid, cmap='gray')
    plt.savefig(img_file)
    plt.close()

if __name__ == '__main__':
    n = noise(500, 50)
    save_image(n, 'test.png')
