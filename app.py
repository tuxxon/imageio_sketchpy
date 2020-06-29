#!/usr/bin/python3

#
# Source from https://github.com/rra94/sketchify
# 

import imageio
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

def dodge(front,back):
    result=front*255/(255-back) 
    result[result>255]=255
    result[back==255]=255
    return result.astype('uint8')

def grayscale(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

img ="http://static.cricinfo.com/db/PICTURES/CMS/263600/263697.20.jpg"

s = imageio.imread(img)
g=grayscale(s)
i = 255-g

b = scipy.ndimage.filters.gaussian_filter(i,sigma=10)
r= dodge(b,g)

plt.imsave('img2.png', r, cmap='gray', vmin=0, vmax=255)