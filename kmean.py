# CORE IMPORTS
import sys
import random
import math
from sklearn.datasets import load_iris
# GRAPHICAL IMPORTS
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sklearn.decomposition import PCA

class ArgError(Exception):
	pass

class Group:
	def __init__(self,rep,col):
		self.r = rep	# Representing Group
		self.g = col	# Real Collection

gDisplay = 0
gEXT = ".txt"
gREP = "files/"

#Checking Arguments
if (len(sys.argv) != 2):
	raise ArgError("usage : kmean.py [K]")

#Getting Arguments
gK = sys.argv[1]

#Checking arguments conformity
try:
	gK = int(gK)
except:
	raise ArgError("[K] must be an integer")

## MAIN ##
repMatrix = load_iris().data

# Calculing matrix size
lPageSize = len(repMatrix)
lVocSize = len(repMatrix[0])

# Checking K is lower than documents size
if lPageSize < gK:
	raise ArgError("[K] "+str(gK)+" is too high => "+str(lPageSize)+" pages")

# -- Display Matrix
print "Representation Matrix:"
for i in range(0,len(repMatrix)):
	print repMatrix[i]
print
	
# -- Initialization
print "Initialization:"
C = [i for i in range(lPageSize)] # Random pages of C will initialize K
newGroupList = []
for i in range(0,gK): # Create K Groups
	random.shuffle(C)
	# We add a document as representation of the group and we add this page in the collection
	newGroupList.append(Group( repMatrix[C[0]], [C[0]] ))
	C = C[1:]
		
	print "Group"+str(i)+" => Doc"+str(newGroupList[i].g[0])
print

counter = 1
while True: #DO WHILE
	if gDisplay:	
		print "## STEP "+str(counter)+":"
	counter += 1
	# -- Storing the current GList
	old = newGroupList
	# -- Calculing next step
	C = [i for i in range(lPageSize)]
	newGroupList = []
	for i in range(0,len(old)): #For Each Group
		# New Group with old representing vector
		newGroupList.append(Group( old[i].r , [] ))

	# -- Add Documents to Groups
	for i in range(0,len(C)):
		scal = []
		# Calculus of scalar for each group
		for j in range(0,len(newGroupList)):		
			scal.append(0)
			diff = [(a_elt - b_elt) **2 for a_elt, b_elt in zip(repMatrix[C[i]], newGroupList[j].r )]
			for el in diff:
				scal[j] += el
		scal = [math.sqrt(p) for p in scal]
	
		# Append doc to the most similar group	
		if gDisplay:
			print "Doc"+str(i)+" => Group"+str(scal.index(min(scal)))
		# Minimum Calculus
		lMin = []
		for it in range(0,len(scal)):
			if scal[it] == min(scal):
				lMin.append(it)
		# Selecting a random minimum scalar
		random.shuffle(lMin)
		newGroupList[lMin[0]].g.append(i)
	if gDisplay:
		print

	# -- Calculing new representant
	for i in range(0,len(newGroupList)): #For Each Group
		newGroupList[i].r = [0 for it in newGroupList[i].r]
		for j in range(0,len(newGroupList[i].g)): #For Each Document of the Group
			newGroupList[i].r = [a_elt + b_elt for a_elt, b_elt in zip(newGroupList[i].r, repMatrix[newGroupList[i].g[j]])]
		newGroupList[i].r = [it/len(newGroupList[i].g) for it in newGroupList[i].r]
		if gDisplay:
			print "Group"+str(i)+":",newGroupList[i].g
			print "R:",newGroupList[i].r
	if gDisplay:
		print

	### WHILE BREAK POINT ###
	bp = True
	for i in range(0,len(old)): #For Each Group
		bp = bp and all( (a_elt-b_elt) == 0 for a_elt, b_elt in zip(old[i].r,newGroupList[i].r) )
	if bp:
		break
## Display last groups
print "Final Groups:"
for i in range(0,len(newGroupList)):
	print "Group"+str(i)+":",newGroupList[i].g
	print "R:",newGroupList[i].r

## Display graphical view
#2D Projection with PCA
pca = PCA(n_components=2)
mat = pca.fit(repMatrix).transform(repMatrix)
#Grouping Docs X and Y
arr = []
for i in range(0,len(newGroupList)): #For Each Group
	xi = []
	yi = []
	for f in newGroupList[i].g: #For Each Doc
		xi.append(mat[f,0])
		yi.append(mat[f,1])
	arr.append(xi)
	arr.append(yi)
#Display Clusters
colors = iter(cm.rainbow(np.linspace(0, 1, len(newGroupList)))) #Colors for clusters
target_names = range(len(newGroupList)) #Label for clusters
plt.figure()
for i in range(0,len(newGroupList)): #For each group
	plt.scatter(arr[2*i], arr[2*i+1], label=target_names[i], color=next(colors))
plt.legend(loc='best')
plt.title('KMeans on IRIS')
plt.show()
