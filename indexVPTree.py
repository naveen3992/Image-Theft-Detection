# import the necessary packages
from PIL import Image
import imagehash
import argparse
import shelve
import glob
import pdb 
import numpy as np
import vptree
import time
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
        # print p1, p2
        # time.sleep(10)
        return bin(p1^p2).count('1')

def arguementinitializer():
    # construct the argument parse and parse the arguments
    #pdb.set_trace()
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required = True, help = "path to input dataset of images")
    ap.add_argument("-s", "--shelve", required = True, help = "output shelve database")
    ap.add_argument("-q", "--query", required = False, help = "path to the query image")
    ap.add_argument("-f","--fname",required = False, help="name of the function to be called")
    ap.add_argument("-r", "--radius", required = False,help = "hamming distance radius")
    args = vars(ap.parse_args())
    return args

# open the shelve database
def create_indices(imageth,databasepath):
    hash_dict = {}
    # loop over the image dataset
    for imagePath in glob.glob(imageth + "/*.jpg"):
        # load the image and compute the difference hash
        image = Image.open(imagePath)
        filename = imagePath[imagePath.rfind("/") + 1:]
        hash_dict[filename] = int(str(imagehash.phash(image)),16)
    hashes = [int(i) for i in hash_dict.values()]
    tree = vptree.VPTree(hashes, euclidean)
    file1 = open(databasepath+"hash_dict.pkl","wb")
    file2 = open(databasepath+"tree.pkl", "wb")
    pickle.dump(hash_dict, file1)
    pickle.dump(tree, file2)
    file1.close()
    file2.close()

def findNearbyImageVPTree(imageFolder, databasefolder, imagepath, hamdist):
    a = time.time()
    file1 = open(databasefolder+'tree.pkl', 'rb')
    datas = pickle.load(file1)
    file2 = open(databasefolder+"hash_dict.pkl","rb")
    datas2 = pickle.load(file2)
    b = time.time()
    print "Time to load: "+str(b-a)
    query = int(str(imagehash.phash(Image.open(imagepath))),16)
    nn =  datas.get_nearest_neighbor(query)
    print "time: "+str(time.time()-b)
    print nn
    key = datas2.keys()[datas2.values().index(nn[1])]
    print key
    image1 = Image.open('/Users/sunilku/Desktop/hackathon/allImagesinone/'+key)
    image1.show()

    image2 = Image.open(imagepath)
    image2.show()

args = arguementinitializer()
if args["fname"] == "create_indices" :
    create_indices(args["dataset"], args["shelve"])
elif args["fname"] == "findDuplicateImage" : 
    findDuplicateImage(args["dataset"],args["shelve"], args["query"])
elif args["fname"] == "findNearbyImage" : 
    findNearbyImage(args["dataset"],args["shelve"], args["query"],args["radius"])
elif args["fname"] == "findNearbyImageVPTree" : 
    findNearbyImageVPTree(args["dataset"],args["shelve"], args["query"],args["radius"])
