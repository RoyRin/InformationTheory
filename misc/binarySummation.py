import numpy

countsOfSeqs = {}
countsOfSeqs['0']=0
countsOfSeqs['1']=0
countsOfSeqs['10']=0
countsOfSeqs['11']=0
countsOfSeqs['00']=0
countsOfSeqs['01']=0

s = ""
def appendNum(n):
	global s
	#global countsOfSeqs
	append = str(bin(n))[2:]
	#print("append"+ append)
	s+=append

def updateCounts():
	global countsOfSeqs
	global s
	for i in range(len(s)):
		for j in range(i):
			#print("i to j"+ str(j) +" "+str(i) +" "+append[j:i])
			if(s[j:i] in countsOfSeqs):
				#print("appending!")
				countsOfSeqs[s[j:i]]+=1

def printSequenceCounts():
	global countsOfSeqs
	for key in countsOfSeqs:

		print(key+ " \t " + str(countsOfSeqs[key]))

for i in range(1000):
	appendNum(i)
updateCounts()

#print(s)
printSequenceCounts()
print("\n\n")

