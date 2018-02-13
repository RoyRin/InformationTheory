import numpy as np
import collections

string = "1010010101011110101001" # 

"""
d = collections.deque('abcdefg')
print 'Deque:', d
print 'Length:', len(d)
print 'Left end:', d[0]
print 'Right end:', d[-1]

d.remove('c')
print 'remove(c):', d """

class pattern:
	count = 0
	pat = ""
	def __init__(self,p,c):
		self.count = c
		self.pat = p
	def getPattern(self):
		return self.pat 
	def getCount(self):
		return self.count

def initialParse2(stringpattern):
	DEQ = collections.deque(stringpattern)
	return DEQ # does not contain counts

def initialParse(stringpattern):
	DEQ = collections.deque()
	for i in range(len(stringpattern)):
		print(i)
		#DEQ.append(pattern(stringpattern[i:i+1], 1))
		p = pattern(stringpattern[i:i+1], 1)
		#print(stringpattern[i:i+1])
		print(p.getPattern(), p.getCount())
	return DEQ

print(initialParse("asdasd"))

def getPnKn(DEQ):
	if(len(DEQ) == 1):
		return

def RHPC_1_(DEQ): #Question - what does a do?
	DEQ = DEQ.reverse()
	a = DEQ.popLeft()
	penUltimate = DEQ.popLeft()
	pat = penUltimate[0]
	count = penUltimate[1]
	k1 = 1
	for i in DEQ:
		if(i.getPattern() == pat):
			k1+=1
		else:
			break
	DEQ.appendLeft(penUltimate)
	DEQ.appendLeft(a)

	DEQtemp = collections.deque()
	length = len(DEQ)
	for i in range(length):
		temp = DEQ.popLeft()
		count = temp.
		for j in range(k1):
			if



	while(len(DEQ) >0):
		temp = DEQ.pop()
		DEQ.append(temp)
		if(temp.getPattern() == pat):
			count+=1
			k1+=1
		else:
			break
	DEQ.append(pattern(pat, count))

	k =1











