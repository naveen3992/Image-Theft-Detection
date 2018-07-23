import vptree
import random
import math
import numpy as np
import time
from PIL import Image
import imagehash
import os
import pickle

def euclidean(p1, p2):
	try:
		return bin(p1^p2).count('1')
	except TypeError:
		# print p1, p2
		p1 = int(p1)
		p2 = int(p2)
		# print p1, p2
		# time.sleep(10)
		return bin(p1^p2).count('1')



hash_dict = {}

file_list = os.listdir("/Users/sunilku/Desktop/hackathon/misc/")
for i in file_list:
	if(i[-3:]=="bmp" or i[-3:]=="jpg"):
		hash_dict[i] = int(str(imagehash.phash(Image.open("/Users/sunilku/Desktop/hackathon/misc/"+i))),16)
		print i, hash_dict[i]

hashes = [int(i) for i in hash_dict.values()]
tree = vptree.VPTree(hashes, euclidean)

file1 = open("hash_dict.pkl","wb")
file2 = open("tree.pkl", "wb")
pickle.dump(hash_dict, file1)
pickle.dump(tree, file2)
file1.close()
file2.close()
