import sys

class ArgError(Exception):
	pass

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
print repMatrix
