
import os
import sys
import numpy as np
import glob
import matplotlib.pyplot as plt

#note - only works if string is size  r^n for some n
#I optimal I = log log n (n size of string)
class MPM:
	r  =2
	I = 5
	x = ""
	U = []
	S=[]
	T = []
	verbose = False
	def __init__(self, s, r, i, v = False):
		self.x = s
		self.r = r
		self.I = i
		self.verbose = v
		self.U = []
		self.S=[]
		self.T = []

	#produce S's
	def multilevel_decomposition_phase(self):
		if(self.verbose):
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
			if(len(self.U[-1][0])<= self.r):
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

		if(self.verbose):
			print("tokeneizainot phase")
			print("length of S"+str(len(self.S)))
		for i in range(len(self.S)):
			self.T.append([])
			if(i== len(self.S)-1):
				self.T[i] = self.S[i]
				break
			a = {}
			count = 0
			if(self.verbose):
				print(str(i)+ " ======")
				print(self.S[i])

			for s in self.S[i]:
				if(self.verbose):
					print("a is "+str(a))

				if(s not in a):
					#print("adding ")
					a[s] = count
					self.T[i].append(count)
					count +=1
				else:
					#print("DO I EVER GET HERE?")
					self.T[i].append(a[s])
			if(self.verbose):
				print("should be 0"+ str(len(self.T[i])-len(self.S[i])))
		if(self.verbose):
			print("T's")
			for i in range(len(self.T)):
				print(self.S[i])
				print(self.T[i])

		return
	def decoding_phase(self):
		a = self.T[0]
		for i in range(1, self.I): # needs to go to self.I	 (otherwise, doesnt' work)	
		
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
		return [l*1.,len(self.x)]



def readFile(fn):
	f = open(fn)
	#print(f.read())
	return(f.read())

def countDifferences(s1,s2):
	print("length difference: "+ str(len(s1)- len(s2)))
	count = 0
	for i in range(min(len(s1),len(s2))):
		if(s1[i]!= s2[i]):
			count+=1

	print("nuber of differences:" + str(count))

def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(toFile, append_write) as f:
        f.write(text)
def plot(name, entropies):
	#manually insert which sizes they are : 2^5, 2^10, 2^15, 2^
	x = [5,6,7,8,9,10,15,17,19,20,21,22]
	x = x[:len(entropies)]
	plt.clf()
	plt.scatter(x,entropies)
	plt.plot(x, entropies)
	#plt.show()
	plt.title("Size vs Entropy for "+ name)
	plt.xlabel("Log(Size) (base 2) ")
	plt.ylabel("Entropy from MPM")

	plt.savefig("entropy_plot"+name+".jpg")
if __name__ == '__main__':

	funcs = ['_generate_const_seq', '_generate_checkerboard_seq', '_generate_random_seq', '_generate_rudin_shapiro_seq',
    '_generate_thue_morse_seq', '_generate_fibonacci_seq', '_generate_baum_sweet_seq', 
    '_generate_dragon_seq', '_generate_ehrenfeucht_mycielski_seq', 'generate_random_seq']
	
	#funcs = ['_generate_const_seq']
	Entropies = {}
	for i in funcs:
		Entropies[i] = []
	print(Entropies)
	for i in funcs:

		print("here")
		print('/Users/Roy/Research/Chaikin/InformationTheory/sequences/'+i+"*")
		for filename in glob.glob('/Users/Roy/Research/Chaikin/InformationTheory/sequences/sequence'+i+"*"):
			print(i+" : ")
			s = readFile(filename)
			print(filename )
			m = MPM(s,2,10)# string, R, I
			m.multilevel_decomposition_phase()
			
			m.tokenization_phase()
			decode = m.decoding_phase()
			decoded = ""
			
			for c in decode:
				decoded+=str(c)
			if(s != decoded):
				print("Decoding not the same as original message! Problemo")
				print(s)
				print(decoded)
				countDifferences(s, decoded)
			e = m.MPM_Entropy()
			del(m)
			print(str(e[0] )+" "+ str(e[1]))

			Entropies[i].append(e[0]*1./(1.*e[1]))# currently a bug - trying to figure out why entropies are 
			#2 times as big as they should be, so i am simply dividing by 2 for the time being
			print(Entropies[i])
		printOut("Entropies.txt", str(i)+ " : "+str(Entropies[i])+"\n")
		plot(i, Entropies[i])

'''
	print(sys.argv)
	if(int(len(sys.argv))>1):
		s= readFile(sys.argv[1])
	power = np.log2(len(s))

	for i in range(4,power,5):
		m = MPM(s,2,10)# string, R, I
		m.multilevel_decomposition_phase()
		
		m.tokenization_phase()
		decode = m.decoding_phase()
		decoded = ""
		
		for i in decode:
			decoded+=str(i)
		if(s != decoded):
			print("Decoding not the same as original message! Problemo")
			print(s)
			print(decoded)
			countDifferences(s, decoded)

		e = m.MPM_Entropy()
	#printOut(sys.argv[1][:-4]+"_Entropy.txt", "Entropy is "+  str(e[0]) + " / "+ str(e[1]) + " : " +str(e[0]*1./e[1]))
	#print("Entropy is "+ str(e))
'''












