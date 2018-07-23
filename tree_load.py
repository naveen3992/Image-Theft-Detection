import vptree
import random
import math
import numpy as np
import time
from PIL import Image
import imagehash
import os
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def euclidean(p1, p2):
	try:
		return bin(p1^p2).count('1')
	except TypeError:
		# print p1, p2
		p1 = int(p1)
		p2 = int(p2)
		return bin(p1^p2).count('1')

a = time.time()

file1 = open('tree.pkl', 'rb')
datas = pickle.load(file1)

file2 = open("hash_dict.pkl","rb")
datas2 = pickle.load(file2)

b = time.time()
print "Time to load: "+str(b-a)
query = int(str(imagehash.phash(Image.open("/Users/sunilku/Desktop/hackathon/blur/damien_hirst_does_fashion_week.bmp"))),16)
nn =  datas.get_nearest_neighbor(query)
print "time: "+str(time.time()-b)
print nn
key = datas2.keys()[datas2.values().index(nn[1])]
print key
img=mpimg.imread('/Users/sunilku/Desktop/hackathon/misc/'+key)
imgplot = plt.imshow(img)
plt.show()


