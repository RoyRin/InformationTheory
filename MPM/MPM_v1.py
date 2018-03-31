

import os
import numpy

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
		# the sequences S0, S1, ...SI(x) are formed
		# each s_i consists of nonoverlapping substrings of x of length r^I-i
		for i in range(self.I):
			dic = {}
			#self.U.append[{}]
			size = (self.r**(self.I-i))
			self.U.append({})
			self.S.append([])
			count =0
			for ii in range(0, len(self.x), size):
				a = self.x[ii : ii+ size]
				if( a not in self.U[i]):

					self.U[i][a] = count
					count+=1
					self.S[i].append(a[:int(len(a)/2)])
					self.S[i].append(a[int(len(a)/2):])
			#self.U.append(dic)
			#self.S.append([self.x[ii : ii+ size] for ii in range(0,len(self.x), size) if self.x[ii : ii+ size] in self.U[i]  ] )
			#for ii in range(len(U[i])):
			#	S[i].append()
#			#print(self.x[0:size])
			#print([self.x[ii : ii+ size] for ii in range(0,len(self.x), size)])
#			self.S.append([self.x[ii: ii+(self.r**(self.I-i)) ] for ii in range(0,len(self.x)),(self.r**(self.I-i))  ])
		return

	#produce Ts
	def tokenization_phase(self):
		for i in range(len(self.S)):
			self.T.append([])
			a = {}
			count = 0
			for s in self.S[i]:
				if(s not in a):
					a[s] = count
					self.T[i].append(count)
					count +=1
				else:
					self.T[i].append(a[s])
		return
	def encoding_phase(self):
		a = self.T[0]
		#print(a)
		for i in range(1, len(self.T)):
			#print("len a ", len(a), "\n")
			for j in range(len(a)):
				#print("from ", self.r*a[j], " to ", (1+a[j])*self.r)
				a[j] = self.T[i][self.r*a[j]:(a[j]+1)*self.r]
				#print(a[j])
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


s = "00100100100000010010000010010010"

m = MPM(s,2,5)
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









