from PIL import Image
import matplotlib.pyplot as plt
import random
import array
import numpy as np

# Get original image and details
pic = 'dogCropped'
filetype = '.jpg'
img = Image.open(pic + filetype)
width, height = img.size

#obtain array for vector implementation
pixelMap = np.asarray(img)
pixelMap = pixelMap/255
#flatten to an array of tuples (each representing a pixel)
pixelsArray = pixelMap.reshape((-1,3))
print(pixelsArray)

# Set variables 
K = 10
m = len(pixelsArray)
iters = 10

# random initialization by choosing a few pixels
def randomInit():
	#create random variables
	randList = [random.randint(0,m-1) for iter in range(K)]
	#select random initial centroids
	initCentroids = [pixelsArray[i] for i in randList]
	return initCentroids

centroids = randomInit()
centroidsArray = np.array(centroids)

idx = np.array([i for i in range(m)])

# assign each point to the closest centroid
def assignCentroids():
	for i in range(m):
		minDist = 1000000
		index = K + 1
		pixel = pixelsArray[i]
		for j in range(K):
			centroid = centroidsArray[j]
			diff = pixel - centroid
			diff = diff * diff
			dist = np.sum(diff, axis=0)
			if dist < minDist:
				minDist = dist
				index = j
		idx[i] = index

#calculate the new centroid positions
def recomputeCentroid():
	for i in range(K):
		indexes = np.array([x for x in range(len(idx)) if idx[x] == i])
		points = np.array([pixelsArray[x] for x in indexes])
		sumPoints = np.sum(points, axis = 0)
		centroid = sumPoints/len(points)
		centroidsArray[i] = centroid

#run the process for "iter" number of times
''' not tested :')
def chooseBestInitCentroids(numTries):
	minDist = 10000
	bestCentroids = randomInit()
	for i in range(numTries):
		tempcentroids = randomInit()
		tempcentroids = np.array(tempcentroids)
		for i in range(iters):
			print("iteration: " + str(i))
			assignCentroids()
			recomputeCentroid()
		centroidAlloc = np.array([tempcentroids[x] for x in idx])
		tempPixelsArray = np.zeros((height*width,3),dtype=int)
		for i in range(m):
			tempPixelsArray[i] = tempcentroids[idx[i]]
		diff = tempPixelsArray - centroidAlloc
		diff = diff*diff
		sumDist = np.sum(np.sum(diff,axis=0),axis=0)
		if sumDist < minDist:
			minDist = sumDist
			bestCentroids = tempcentroids
	print("best centroid chosen")
	return bestCentroids

#comment out this if just want to do 1 iteration
#centroids = chooseBestInitCentroids(3);
#centroidsArray = np.array(centroids)
'''


assignCentroids()

for i in range(iters):
	print("iteration: " + str(i))
	assignCentroids()
	recomputeCentroid()

newPixelsArray = np.zeros((height*width,3), dtype = int)

for i in range(m):
	newPixelsArray[i] = centroidsArray[idx[i]]*255


newPixelsArray = np.reshape(newPixelsArray, (height,width,3))
newImg = Image.fromarray(newPixelsArray.astype(np.uint8))
newImg.save(pic + '_Compressed_' + str(K) + 'colours.jpg')
newImg.show()
