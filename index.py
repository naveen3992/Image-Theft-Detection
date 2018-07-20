# import the necessary packages
from PIL import Image
import imagehash
import argparse
import shelve
import glob
import pdb 

def arguementinitializer():
    # construct the argument parse and parse the arguments
    #pdb.set_trace()
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required = True, help = "path to input dataset of images")
    ap.add_argument("-s", "--shelve", required = True, help = "output shelve database")
    ap.add_argument("-q", "--query", required = False, help = "path to the query image")
    ap.add_argument("-f","--fname",required = False, help="name of the function to be called")
    args = vars(ap.parse_args())
    return args

# open the shelve database
def create_indices(imageth,databasepath):
    #pdb.set_trace()
    db = shelve.open(databasepath, writeback = True)
    # loop over the image dataset
    for imagePath in glob.glob(imageth + "/*.jpg"):
        # load the image and compute the difference hash
        image = Image.open(imagePath)
        h = str(imagehash.phash(image)) #navkuma -  changed from dhash to phash 

        # extract the filename from the path and update the database
        # using the hash as the key and the filename append to the
        # list of values
        filename = imagePath[imagePath.rfind("/") + 1:]
        db[h] = db.get(h, []) + [filename]

    # close the shelf database
    db.close()


def findDuplicateImage(imageFolder, databasefolder, imagepath):
    # open the shelve database
    db = shelve.open(databasefolder)
    # load the query image, compute the difference image hash, and
    # and grab the images from the database that have the same hash
    # value
    query = Image.open(imagepath)
    h = str(imagehash.phash(query)) #navkuma - changed from dhash to phash
    filenames = db[h]
    print "Found %d images" % (len(filenames))
    # loop over the images
    for filename in filenames:
        image = Image.open(imageFolder + "/" + filename)
        image.show()
    # close the shelve database
    db.close()




args = arguementinitializer()
if args["fname"] == "create_indices" :
    create_indices(args["dataset"], args["shelve"])
elif args["fname"] == "findDuplicateImage" : 
    findDuplicateImage(args["dataset"],args["shelve"], args["query"])
