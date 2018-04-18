
import os
import sys
import numpy as np
#note - only works if string is size  r^n for some n

#I optimal I = log log n (n size of string)
class MPM:
	r  =2
	I = 5
	x = ""
	U = []
	S=[]
	T = []

	def __init__(self, s, r, i):
		self.x = s
		self.r = r
		self.I = i

	#produce S's
	def multilevel_decomposition_phase(self):
		print("string is "+self.x)
		# the sequences S0, S1, ...SI(x) are formed
		# each s_i consists of nonoverlapping substrings of x of length r^I-i
		
		self.U.append([self.x])
		count = 0
		size = len(self.x)
		self.I = 1
		while(True):
			size = int(size/self.r)
			i = self.I
			#print("iterations"+ str(i))
			dic = {}
			self.U.append([])
			count =0
			for ii in range( len(self.U[i-1])):
				for rr in range(self.r):
					a = self.U[i-1][ii][rr*(size):(rr+1)*(size)]
					if( a not in dic):
						dic[a] = count
						count+=1
						self.U[i].append(a)
						n = int(len(a)/self.r )	
			#self.S[-1] = [item for sublist in self.S[-1] for item in sublist] # flatten S into 1 array
			#print("size of 1 unit of U"+ str(len(self.U[-1][0])))
			self.I +=1
			if(len(self.U[-1][0])== self.r):
				break
		for l in range(len(self.U)):
			self.S.append([])
			for z in range(len(self.U[l])):
				n = int(len(self.U[l][z])/self.r )
				a = [self.U[l][z][i:i+n] for i in range(0, len(self.U[l][z]), n)]
				self.S[-1].append(a)
			self.S[-1] = [item for sublist in self.S[-1] for item in sublist] # flatten S into 1 array
		
		'''
		print("I is "+ str(self.I))
		print("u"+ str(len(self.S)))
		for i in self.U:
			print(i)
			print(len(i))
		
		print("SSSSS")
		for i in self.S:
			print(i)
			print(len(i))
		'''
		return


	#produce Ts
	def tokenization_phase(self):
		print("tokeneizainot phase")
		print("length of S"+str(len(self.S)))
		for i in range(len(self.S)):
			self.T.append([])
			a = {}
			count = 0
			print(str(i)+ " ======")
			print(self.S[i])

			for s in self.S[i]:
				print("a is "+str(a))
				#print(a)
				#print(s)
				if(s not in a):
					#print("adding ")
					a[s] = count
					self.T[i].append(count)
					count +=1
				else:
					#print("DO I EVER GET HERE?")
					self.T[i].append(a[s])
			print("should be 0"+ str(len(self.T[i])-len(self.S[i])))
		print("T's")
		for i in range(len(self.T)):
			print(self.S[i])
			print(self.T[i])

		#print(self.T)
		return
	def encoding_phase(self):
		a = self.T[0]
		for i in range(1, self.I): # needs to go to self.I+1	 (otherwise, doesnt' work)	
		
			#print("len a ", len(a), "\n")
			for j in range(len(a)):
				temp = []
				for rr in range(self.r):
					temp.append(self.T[i][(self.r*a[j])+rr])
				a[j] = temp

			a = [item for sublist in a for item in sublist] # flatten a
		return a
#		print(a)
	def MPM_Entropy(self):
		l =0
		for i in range(len(self.T)):
			for s in (self.T[i]):
				l+= len(str(s))

		print("Entropy is " + str(l) + " / "+ str(len(self.x)))
		return (l*1./len(self.x))
def readFile(fn):
	f = open(fn)
	#print(f.read())
	return(f.read())
if __name__ == '__main__':
	
	s = "00100100100000010010000010010010"
	print(sys.argv)
	if(int(len(sys.argv))>1):
		s= readFile(sys.argv[1])
		#s = sys.argv[1]
	print(s)
	print(int(np.log2(np.log2(len(s)))) )
	m = MPM(s,2,10)# string, R, I
	m.multilevel_decomposition_phase()
	
	m.tokenization_phase()
	decode = m.encoding_phase()
	decoded = ""
	
	for i in decode:
		decoded+=str(i)
	print(decoded)
	print(s)
	e = m.MPM_Entropy()
	print("Entropy is "+ str(e))

	
	#


