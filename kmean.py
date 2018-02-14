import sys
import random
import math

class ArgError(Exception):
	pass

class Group:
	def __init__(self,rep,col):
		self.r = rep	# Representing Group
		self.g = col	# Real Collection

gEXT = ".txt"
gREP = "files/"

#Checking Arguments
if (len(sys.argv) != 3):
	raise ArgError("usage : kmean.py [K] [FileName]")

#Getting Arguments
gK = sys.argv[1]
gFName = sys.argv[2]

#Checking arguments conformity
try:
	gK = int(gK)
except:
	raise ArgError("[K] must be an integer")

if not ((gFName.endswith(gEXT) and ("." not in gFName[:-len(gEXT)])) or ("." not in gFName)):
	raise ArgError("[FileName] has unsupported extension => use "+gEXT)
if not (gFName.startswith(gREP) or ("/" not in gFName)):
	raise ArgError("[FileName] has unsupported path => use "+gREP)

# Conforming gFName
if ("." not in gFName):
	gFName = gFName + gEXT
if not (gFName.startswith(gREP)):
	gFName = gREP + gFName

## MAIN ##
repMatrix = []
with open(gFName, "r") as gFile:
	lFirstLine = gFile.readline().split(",")
	lPageSize = int(lFirstLine[0])
	lVocSize = int(lFirstLine[1])

	if lPageSize < gK:
		raise ArgError("[K] "+str(gK)+" is too high for "+sys.argv[2]+" => "+str(lPageSize)+" pages")

	# For each page	
	for j in range(0,lPageSize):
		ligne = gFile.readline().split(" ")	
		ligneflt = []
		# For each word
		for i in range(1,lVocSize+1):
			ligneflt.append(0) #0 in any case
			for el in range(1,len(ligne)):
				if (ligne[el].startswith(str(i)+":")): #If words[i] is in page
					ligneflt[i-1] = float(ligne[el][2:]) #We replace 0 by prob
					break
		repMatrix.append(ligneflt)

# -- Display File as Matrix
print "Representation Matrix:"
for i in range(0,len(repMatrix)):
	print repMatrix[i]
print
	
# -- Initialization
print "STEP 0:"
C = [i for i in range(lPageSize)] # Random pages of C will initialize K
newGroupList = []
for i in range(0,gK): # Create K Groups
	random.shuffle(C)
	# We add a document as representation of the group and we add this page in the collection
	newGroupList.append(Group( repMatrix[C[0]], [C[0]] ))
	C = C[1:]
		
	print "Group"+str(i)+" => Doc"+str(newGroupList[i].g[0])
	print "R:",newGroupList[i].r
print

counter = 1
while True: #DO WHILE
	print "STEP "+str(counter)+":"
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
		print "Doc"+str(i)+" => Group"+str(scal.index(min(scal)))
		newGroupList[scal.index(min(scal))].g.append(i)
	print

	# -- Calculing new representant
	for i in range(0,len(newGroupList)): #For Each Group
		newGroupList[i].r = [0 for it in newGroupList[i].r]
		for j in range(0,len(newGroupList[i].g)): #For Each Document of the Group
			newGroupList[i].r = [a_elt + b_elt for a_elt, b_elt in zip(newGroupList[i].r, repMatrix[newGroupList[i].g[j]])]
		newGroupList[i].r = [it/len(newGroupList[i].g) for it in newGroupList[i].r]
		print "Group"+str(i)+":",newGroupList[i].g
		print "R:",newGroupList[i].r
	print

	### WHILE BREAK POINT ###
	bp = True
	for i in range(0,len(old)): #For Each Group
		bp = bp and all( (a_elt-b_elt) == 0 for a_elt, b_elt in zip(old[i].r,newGroupList[i].r) )
	if bp:
		break
