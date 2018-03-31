import re
import numpy as np



class node: # will take a linked list approach to compression - should be in line (O(n) memory)
	ind = -1
	a = 0 #inclusive
	b= 1 # exclusive
	children = 0
	prev= None
	next = None
	def __init__(self, a,b,c):
		self.a = a
		self.b = b
		self.children = c

	def set_next(self,n):
		self.next = n
	def get_next(self):
		return self.next

	def eat_next(self): # in line merging of the linked list - has one node, absorbs the node to its right
		if(self.next == None):
			return
		self.children +=1
		self.b = self.next.b
		if(self.next.next == None): # 2nd from the end
			self.next = None # move to the end, don't set the reverese driection
			return

		self.next.next.prev = self # se
		self.next = self.next.next
		# children need to be set external to this method, because, it is unknown how many eat nexts, will occur
		# 

	def set_children(self,c): # keep track of how many things merged into that thing
		self.children =c
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
		self.head = node(0,1,0)
		self.head.ind = 0
		temp = self.head
		self.size = len(s)
		for i in range(1, len(s)):
			temp.ind = i
			temp.next = node(i,i+1,0)
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

		while(self.s[n.a:n.b] == currentP):
			n = n.prev
			currentK +=1
			if(n == None):
				break
			

		self.k.append(currentK)

		n = self.ll.head # n is a temp node, which will go forward, looking to merge possible nodes, each round for the given k, p combo
		#print("k is " + str(currentK) + " p is " +str(currentP))
		while (n != None):
			if(self.s[n.a:n.b] != currentP):
				n = n.next
				continue
			temp = n.next # if the node matches the correct pattern, it should look ahead to see how many of the nodes it should eat
			kk=1
			for i in range(currentK-1): #only should check to match at most k spots though!
				if(temp == self.ll.tail):
					break
				if(self.s[temp.a:temp.b] != currentP):
					break
				kk+=1
				temp = temp.next
			#print("kk is ", kk)
			#print("n is "+ self.s[n.a:n.b])
			n.set_children(0)
			if(kk == 0):
				print("omg !!!!! kk = 0")
			for i in range(kk):
				n.eat_next()

			self.ll.size = self.ll.size - kk 
			n.set_children(kk)

			if(n.next == None):
				self.ll.tail = n
			n = n.next

		self.symbols.append(currentP)
		print("head children:" + str(self.ll.head.children) + str(self.ll.size))
		
		a = 0
		if(self.ll.size >1):
			a = self.ll.tail.children
		else:
			a = self.ll.head.children
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

#s = "0123456789"

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

t.printCompression()

print("t complexity: "+ str(t.T_complexity()) + " ratio per symbol: " +str(t.T_complexity()/len(t.s)*1.) )
compression = t.printCompressionString()[0]
print(s)
print(compression)
print("compression from "+ str(len(s)) + " to ~" + str(len(compression)))







