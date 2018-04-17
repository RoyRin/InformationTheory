

import os
import sys
import numpy as np

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
		#n = int(len(self.x)/self.r )
		#self.S.append([self.x[i:i+n] for i in range(0, len(self.x), n)])
		#for i in range(1, self.I):
		while(True):
			size = int(size/self.r)
			i = self.I
			print("iterations"+ str(i))
			dic = {}
			#self.U.append[{}]
			#size = (self.r**(self.I-i))
			self.U.append([])
			#self.S.append([])
			count =0
			for ii in range( len(self.U[i-1])):
				#size = int(len(self.U[i-1][0])/self.r)
				#print(size)
				for rr in range(self.r):
					a = self.U[i-1][ii][rr*(size):(rr+1)*(size)]
					if( a not in dic):
						dic[a] = count
						count+=1
						self.U[i].append(a)

						n = int(len(a)/self.r )
						#self.S[-1].append([a[i:i+n] for i in range(0, len(a), n)])
							
					#for rrr in range(self.r):
					#	a = self.U[i-1][ii][rrr*(size):(rrr+1)*(size)]
					#	self.S[i-1].append(a)
			
			#self.S[-1] = [item for sublist in self.S[-1] for item in sublist] # flatten S into 1 array
			print("size of 1 unit of U"+ str(len(self.U[-1][0])))
			self.I +=1
			if(len(self.U[-1][0])== self.r):
				break
		
		
		for l in range(len(self.U)):
			self.S.append([])
			for z in range(len(self.U[l])):
				n = int(len(self.U[l][z])/self.r )
				a = [self.U[l][z][i:i+n] for i in range(0, len(self.U[l][z]), n)]
				#print("n is "+ str(n))
				#print("a is "+ str(a))
				self.S[-1].append(a)
			self.S[-1] = [item for sublist in self.S[-1] for item in sublist] # flatten S into 1 array
		
		self.I -=1
		print("I is "+ str(self.I))
		print("u"+ str(len(self.S)))
		for i in self.U:
			print(i)
			print(len(i))
		
		print("SSSSS")
		for i in self.S:
			print(i)
			print(len(i))
		
		return
		'''
		def multilevel_decomposition_phase(self):
		# the sequences S0, S1, ...SI(x) are formed
		# each s_i consists of nonoverlapping substrings of x of length r^I-i
		self.S.append([self.x])
		self.U.append({self.x})
		for i in range(1, self.I):
			dic = {}
			#self.U.append[{}]
			size = (self.r**(self.I-i))
			self.U.append({})
			self.S.append([])
			count =0
			for ii in range(0, len(self.S[i-1])):
				size = int(len(self.S[i-1][0])/self.r)
				for rr in range(self.r):
					a = self.S[i-1][ii][rr*(size):(rr+1)*(size)]

					if( a not in self.U[i]):
						self.U[i][a] = count
						count+=1
						self.S[i].append(a)
						
				#print(self.S[i])
			#self.U.append(dic)
			#self.S.append([self.x[ii : ii+ size] for ii in range(0,len(self.x), size) if self.x[ii : ii+ size] in self.U[i]  ] )
			#for ii in range(len(U[i])):
			#	S[i].append()
#			#print(self.x[0:size])
			#print([self.x[ii : ii+ size] for ii in range(0,len(self.x), size)])
#			self.S.append([self.x[ii: ii+(self.r**(self.I-i)) ] for ii in range(0,len(self.x)),(self.r**(self.I-i))  ])
		for i in self.S:
			print(i)
		return
		'''

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
		#print(a)
#		for i in range(1, len(self.T)):
		print("length of T"+ str(len(self.T)))
		for i in range(1, self.I+1): # needs to go to self.I+1	 (otherwise, doesnt' work
			)	
			print("iteratopm"+ str(i))	
			print("a is "+ str(a)+" prior")
			'''
			unique = 0
			maxxer = -1
			for k in range(len(self.T[i])):
				if(self.T[i]>maxxer):
					unique +=1
					maxxer = self.T[i]
			'''
			#print("len a ", len(a), "\n")
			for j in range(len(a)):
				#print("from ", self.r*a[j], " to ", (1+a[j])*self.r)
				temp = []
				for rr in range(self.r):
					temp.append(self.T[i][(self.r*a[j])+rr])
				a[j] = temp
				#a[j] = self.T[i][self.r*a[j]:(a[j]+1)*self.r]
				#print(a[j])
			print("a is "+ str(a))
			a = [item for sublist in a for item in sublist] # flatten a
			print("level i", str(i), a)
		return a
#		print(a)
"""
	def encoding_phase(self):
		a = self.T[0]
		print(a)
		for i in range(1,len(self.T)-1):# for each T
			count = 0
			tempdict = {}
			for j in range(len(a)): # do the CFG decryption 
				temp = []
				if(a[j] not in tempdict):
					tempdict[a[j]] = count
					for q in range(self.r):
						temp.append(self.T[i][(self.r*count)+q ])
					count+=1

				a[j] = temp
			a = [item for sublist in a for item in sublist] # flatten a
			print("level i", str(i), a)
		#print("AAHAHAHAHAHHAHHA", a)
		#print(a)
"""
if __name__ == '__main__':
	s = "00100100100000010010000010010010"
	print(sys.argv)
	if(int(len(sys.argv))>1):
		s = sys.argv[1]
	print(s)
	print(int(np.log2(np.log2(len(s)))) )
	m = MPM(s,2,5)# string, R, I
	m.multilevel_decomposition_phase()
	
	m.tokenization_phase()
	decode = m.encoding_phase()
	decoded = ""
	
	for i in decode:
		decoded+=str(i)
	print(decoded)
	print(s)

	'''
	for i in range(len(m.S)):
		#print(m.U[i])
		print("S" + str(i))
		print(m.S[i])

	for i in range(len(m.T)):
		#print(m.U[i])
		print("T" + str(i))
		print(m.T[i])

	'''






'''
T's
['00100100', '10000001', '00100000', '10010010']
[0, 1, 2, 3]
['0010', '0100', '1000', '0001', '0010', '0000', '1001', '0010']
[0, 1, 2, 3, 0, 4, 5, 0]
['00', '10', '01', '00', '10', '00', '00', '01', '00', '00', '10', '01']
[0, 1, 2, 0, 1, 0, 0, 2, 0, 0, 1, 2]
['0', '0', '1', '0', '0', '1']
[0, 0, 1, 0, 0, 1]

['0010010010000001', '0010000010010010']
[0, 1]
['00100100', '10000001', '00100000', '10010010']
[0, 1, 2, 3]
['0010', '0100', '1000', '0001', '0010', '0000', '1001', '0010']
[0, 1, 2, 3, 0, 4, 5, 0]
['00', '10', '01', '00', '10', '00', '00', '01', '00', '00', '10', '01']
[0, 1, 2, 0, 1, 0, 0, 2, 0, 0, 1, 2]
['0', '0', '1', '0', '0', '1']
[0, 0, 1, 0, 0, 1]
'''

