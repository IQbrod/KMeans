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
with open(gFName, "r") as gFile:
	lFirstLine = gFile.readline().split(",")
	#We ignore lFirstLine[0] that represents the amout of documents into the collection
	lVocSize = int(lFirstLine[1])
	print lVocSize
