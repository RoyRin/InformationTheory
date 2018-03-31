'''
What is the goal here: the goal is that during the t code generation process, you store which symbols 
generated the next p value. 
Then in compression, rather than storing the entire string of characters from the original alphabet
you store which previous values were concated to form the next p.

This works because the process of creating a t-code, ensures that each p, will be used sequentially
one after the other, in the same order that they were generated. The largest one last. The last code 
that is generated, is the first in the sequence. Which means, that in compression, if we store the values of
each p, and specifically how it was generated - then as we are decompressing, if we decompress from the back, forward,
then (left to right) we can store which symbols generated the following p.

This would allow for some compression, because you would simply be storing pointers to the previous p's which
generate this p. In order to store these pointers, rather than writing characters from the alphabet
you can write down the count, at which that symbol appeared previously.
	- for each p, in order to record the p's that generated it, you would only need to store the pointer 
		to the previous p, which could be identified uniquely in log_2 |num P| bits, where |num P| 
		is the number of p's up to that point.

		You would only need to store: 1 p-pointer (log_2 |num P| bits ) + 1 k-value + 1 p-pointer (log_2 |num P| bits )
				(since the process of creating a p, is you take a chain of previous p's + 1 more characters



'''

import re
import numpy as np

class node: # will take a linked list approach to compression - should be in line (O(n) memory)
	ind = -1
	a = 0 #inclusive
	b= 1 # exclusive
	num_children = 0
	children_p = []
	children_k = []
	prev= None
	next = None
	def __init__(self, a,b,numChildren, childrenp, childrenk):
		self.a = a
		self.b = b
		self.num_children = numChildren
		self.children_p = childrenp
		self.children_k = childrenk


	def set_next(self,n):
		self.next = n
	def get_next(self):
		return self.next

	def eat_next(self): # in line merging of the linked list - has one node, absorbs the node to its right
		if(self.next == None):
			return
		self.num_children +=1
		self.b = self.next.b
		self.children_p.extend(self.next.children_p)
		self.children_k.extend(self.next.children_k)
		if(self.next.next == None): # 2nd from the end
			self.next = None # move to the end, don't set the reverese driection
			return

		self.next.next.prev = self # se
		self.next = self.next.next
		#self.
		# children need to be set external to this method, because, it is unknown how many eat nexts, will occur
		# 
	def set_children_p(self, cp):
		self.children_p = cp

	def set_children_k(self, ck):
		self.children_k = ck

	def set_children_count(self,c): # keep track of how many things merged into that thing
		self.num_children =c

	def set_next(self,n):
		self.next = n

	def set_prev(self,p):
		self.prev = p


class linked_list:
	head = None
	tail= None
	size = 0
	string = ""
	def __init__(self, s):
		self.string = s
		self.head = node(0,1,0,[],[])
		self.head.ind = 0
		temp = self.head
		self.size = len(s)
		for i in range(1, len(s)):
			temp.ind = i
			temp.next = node(i,i+1,0,[],[])
			temp.next.prev = temp
			temp = temp.next
		temp.ind = len(s)	
		self.tail = temp

	def print_listnodes(self):

		temp = self.head
		print("Head "+ str(self.head.a) + " to " + str(self.head.b))
		print("Tail "+ str(self.tail.a) + " to " + str(self.tail.b))
		while (temp != self.tail):
			print(str(temp.a)+ " to " + str(temp.b)  +" : "+ self.string[temp.a:temp.b])
			temp = temp.next
		print(str(self.tail.a)+ " to " + str(self.tail.b) +" : "+ self.string[self.tail.a:self.tail.b])

		print("\n\n\n")
		temp = self.head
		while (temp != None):
			print("node " + str(temp.ind) )
			print(str(temp.a)+ " to " + str(temp.b)  +" : "+ self.string[temp.a:temp.b])
			print("\tprevious:")
			if(temp.prev != None):
				print("\t" + str(temp.prev.ind))
			print("\tnext:")
			if(temp.next != None):
				print("\t"+ str(temp.next.ind))
			temp = temp.next
	def print_listnodes_short(self):

		temp = self.head
		
		while (temp != None):
			print("node " + str(temp.ind) )
			print(str(temp.a)+ " to " + str(temp.b)  +" : "+ self.string[temp.a:temp.b])
		
			temp = temp.next
		print("\n \n ")
class TCode:
	symbols = []
	exponents = []
	k = []
	s = ""
	ll = None
	
	penultimate = None
	currentK = 0
	currentP = ""


	def __init__(self, string):
		self.s = string
		self.ll = linked_list(string)

	def compress(self):
		#print("size is " +str(self.ll.size))
		self.penultimate = self.ll.tail.prev
		#print("index of penultimate: " + str(self.penultimate.ind))
		
		currentP = self.s[self.penultimate.a:self.penultimate.b]


		#self.exponents.append(penultimate.children)
		
		n = self.penultimate

		currentK =0
		#this is used to figure out the k (you do a search from right to left from the penultimate)
		while(self.s[n.a:n.b] == currentP):
			n = n.prev
			currentK +=1
			if(n == None):
				break
			

		self.k.append(currentK)

		n = self.ll.head # n is a temp node, which will go forward, looking to merge possible nodes, each round for the given k, p combo
		#print("k is " + str(currentK) + " p is " +str(currentP))
		while (n != None): # while you can compress the t-codes into smaller nodes, continue to do so
			if(self.s[n.a:n.b] != currentP):  # if node is not the same as currentP, leave it alone
				n = n.next
				continue
			temp = n.next # if the node matches the correct pattern, it should look ahead to see how many of the nodes it should eat
			kk=1
			'''
			tempk_count =0
			n.set_children_count(0)
			for i in range(currentK-1): #only should check to match at most k spots though!
				if(temp == self.ll.tail):
					break
				n.eat_next()
				temp = temp.next
				
				if(self.s[temp.a:temp.b] != currentP):
					break

				tempk_count +=1
				kk+=1
				
			#print("kk is ", kk)
			#print("n is "+ self.s[n.a:n.b])
			
			if(kk == 0):
				print("omg !!!!! kk = 0")



			'''
			for i in range(currentK-1): #only should check to match at most k spots though!
				if(temp == self.ll.tail):
					break
				if(self.s[temp.a:temp.b] != currentP):
					break
				kk+=1
				temp = temp.next
			#print("kk is ", kk)
			#print("n is "+ self.s[n.a:n.b])
			n.set_children_count(0)
			if(kk == 0):
				print("omg !!!!! kk = 0")

			#BeepBoopBaap - I belive that I can merge this with the for loop above - I don't know
			#why you would do 2 separate loops
			# however, when i merge the two shits, it stops working
			tempk_count = 0 # keep track of how many iterations this merge actually does
			lastPs = []
			lastKs = []
			for i in range(kk):
				if(n.next != None):
					lastPs = n.next.children_p
					lastKs = n.next.children_k
				n.eat_next()
				tempk_count +=1
			#n.next()
			#n.set_children_p([currentP].extend(lastPs))
			#n.set_children_k([tempk_count].extend(lastKs))
			'''  '''

			
			#a =[currentP].extend()
			#n.set_children_p([currentP, BEEPBOOPBAAP]) # HOW DO YOU SET THE APPENDING "CHILDREN_P THING!"
			#n.set_children_k = [tempk_count,1]

			self.ll.size = self.ll.size - kk 
			n.set_children_count(kk)

			if(n.next == None):
				self.ll.tail = n
			n = n.next

		self.symbols.append(currentP)
		print("head children:" + str(self.ll.head.num_children) + str(self.ll.size))
		
		a = 0
		if(self.ll.size >1):
			a = self.ll.tail.num_children
		else:
			a = self.ll.head.num_children
		self.exponents.append(a)
		print("the new size is "+ str(self.ll.size))

	def run_T_codes(self):
		verbose = True
		count = 0
		self.ll.print_listnodes_short()
		while(self.ll.size >1):
			count +=1
			
			self.compress()
			if(verbose):
				print("compression" + str(count))
				print("nodes:")
				self.ll.print_listnodes_short()

		print("K then symbols and then exponents:")
		
		print(self.k)
		print(self.symbols)
		print(self.exponents)
		return [ self.k, self.symbols, self.exponents]

	def T_complexity(self):
		ret = 0.
		for i in range(len(self.k)):
			ret += np.log2(1+self.k[i])
		print("length is "+ str(len(self.k)))
		return ret

	def printCompression(self):
		n = len(self.symbols)
		for i in range(len(self.symbols)):
			print(" (" +str(self.symbols[n-i-1])+ ")^"+str(self.exponents[n-i-1]), end='')
		print(" + "+self.s[-1])

	def printCompressionString(self):
		n = len(self.symbols)
		comp =""
		compNoSpace = ""
		for i in range(len(self.symbols)):
			comp += str(self.symbols[n-i-1])+"."
			compNoSpace+=str(self.symbols[n-i-1])
		comp+=s[-1]+ "!" # symbols, seperated by !, followd by their exponents in binary format
		for i in range(len(self.symbols)):
			comp += str(bin(self.exponents[n-i-1]))[2:]+"." # exponents represented in binary
			compNoSpace += str(bin(self.exponents[n-i-1]))[2:]
		comp+="!"
		return [comp, compNoSpace]
	


def generateRandomString(n):
	s = ""
	for i in range(n*5):
		s+= str(np.random.randint(0,2))
	return s
def generateAll1(n):
	s = ""
	for i in range(n*5):
		s+= str(1)
	return s
def generateOrderedString(n):
	s = ""
	for i in range(n):
		for j in range(5):
			if(i%2 == 0):
				s += str(1)
			else:
				s+=str(0)
	return s


if __name__ == '__main__':
	s= "101101"
	s = "1,10,11,101,1000,1101,10101,100010,110111,1011001"
	s = "1101110110001101101011000101101111011001"
	szartosht = "10011010110111001001101001110101011001010101101100000110100100110100011011001101001011010100101101101011001110100101011010110010100110101001011010100000010001110001001110101010000010010111100010000010110100011001010101101010100000101111"
	#s = "1101110101010"
	#s= szartosht
	s= generateRandomString(100)
	#s = "0100010101101"
	#s= szartosht
	#s= generateAll1(100)
	l = linked_list(s)
	#l.print_listnodes()



	t = TCode(s)


	#t.compress()
	print("\n \n butts")
	t.run_T_codes()
	print("\n\n\n\n")

	#t.printCompression()

	#print("t complexity: "+ str(t.T_complexity()) + " ratio per symbol: " +str(t.T_complexity()/len(t.s)*1.) )
	compression = t.printCompressionString()[0]
	#print(s)
	print(compression)
	print("\n\n\n\n\n\n")
	
	
	print("compression from "+ str(len(s)) + " to ~" + str(len(compression)))














