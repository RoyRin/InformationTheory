import numpy as np

import re

import numpy as np

import re

string = "1010010101011110101001"  #


class node:
    a = 0  # inclusive
    b = 1  # exclusive
    pattern = ""
    symbol = ""
    repeats = 1
    children = []

    symbolType = False

    def __init__(self, from_, to_, p, c):
        self.a = from_
        self.b = to_
        self.pattern = p
        self.repeats = c
        self.children = []
        self.symbol = ""

    def add_child(self, node):
        self.children.append(node)

    def set_pattern(self, p):
        self.pattern = p

    def get_children(self):
        return self.children

    def get_num_children(self):
        return len(self.children)

    def print_children(self):
        for i in range(len(self.children)):
            print(self.children[i].pattern + " ", end='')
        print()


def initialize_nodes(string):
    nodes = []
    for i in range(len(string)):
        nodes.append(node(i, i + 1, string[i:i + 1], 1))
    return [nodes, ""]


def get_repeating_pattern_type(node):
    # does a BFS, searching for the pattern which is repeated
    queue = node.get_children()
    while (queue):
        n = queue.pop(0)
        if (n.symbolType):
            return n
        children = n.get_children()
        for i in range(len(children)):
            queue.append(children[i])


def merge_nodes(nodes, mergeStart, mergeEnd, symb):
    pat = ""
    # print("merging from"+ str(mergeStart) + " to "+ str(mergeEnd))
    n = node(nodes[mergeStart].a, nodes[mergeEnd].b, "", mergeEnd - mergeStart)
    # print("children1 " + str(n.getNumChildren()))
    allSameType = True
    for i in range(mergeStart, mergeEnd + 1):  # inclusive
        #		if( pat != nodes[i].pattern):#
        #			allSameType = False
        pat += nodes[i].pattern
        n.add_child(nodes[i])
        nodes[i].repeats = mergeEnd - mergeStart
    n.set_pattern(pat)
    #	if(allSameType):
    #		print("all the same type! \t \t !!!")
    #	n.symbolType = allSameType

    n.symbol = symb
    # print("children2 " + str(n.getNumChildren()))
    return n


def merge_t_codes(nodes, string):
    n = len(nodes)
    if (n == 1):
        return
    pat = nodes[-2].pattern
    k = 1
    i = 1
    while ((n - 2) - i >= 0):
        if (nodes[n - 2 - i].pattern == pat):
            k += 1
        else:
            break
        i += 1
    # now we have k, now begin merge from R to L
    newNodes = []
    merges = 0
    mergeStart = 0
    mergeEnd = 0
    merging = False
    ki = 0
    # print(n)
    for i in range(0, n):
        # print("i is "+ str(i))
        if (nodes[i].pattern == pat):
            if (ki < k):  # don't merge more than k at a time
                if (merging):
                    mergeEnd += 1
                else:
                    merging = True
                    mergeStart = i
                    mergeEnd = i + 1
                ki += 1
            else:
                newNodes.append(merge_nodes(nodes, mergeStart, mergeEnd, pat))
                ki = 0
                merging = False
        else:
            if (merging):
                newNodes.append(merge_nodes(nodes, mergeStart, mergeEnd, pat))
            else:
                n = node(nodes[i].a, nodes[i].b, nodes[i].pattern, nodes[i].repeats)
                n.symbol = pat
                for i in nodes[i].get_children():
                    n.add_child(i)
                newNodes.append(n)
            merging = False
            ki = 0

    return [newNodes, pat]


def print_nodes(nodes):
    for i in range(len(nodes)):
        print(nodes[i].pattern + " ", end='')
    print()


def print_t_code_pattern(tcodes, string):
    # does a BFS, searching for the pattern which is repeated
    print("printing T code pattern")
    exponents = []
    symbols = tcodes[1]
    queue = tcodes[0][0][0].get_children()
    TCodeComplexity = 0
    a = 1
    symbolIndex = 1
    #	print(symbols)
    symbol = symbols[-1 * symbolIndex]
    while (queue):
        if (symbolIndex > len(symbols)):
            print(" + " + string[-1:])
            return [TCodeComplexity, [symbols, exponents]]
        symbol = symbols[-1 * symbolIndex]
        a += 1
        n = queue.pop(0)
        if (n.pattern == symbol):
            print("(" + n.pattern + ")" + "^" + str(n.repeats) + " ", end='')
            exponents.append(n.repeats)
            symbolIndex += 1
            TCodeComplexity += np.log2(1 + n.repeats)
            continue
        children = n.get_children()
        for i in range(len(children)):
            queue.append(children[i])

    return [TCodeComplexity, [symbols, exponents]]


def t_code_it_up(string):
    n = initialize_nodes(string)
    symbols = []
    print_nodes(n[0])
    while (len(n[0]) > 1):
        n = merge_t_codes(n[0], string)
        print_nodes(n[0])
        symbols.append(n[1])
        print("p =" + str(n[1]))
        print()
    print(" symbols")
    print(symbols)
    return [n, symbols]


def naiveCompression(symbols, string):# this will simply run tcodeitup,
	# and then iterate through the symbols, left to right
	for i in range(len(symbols)):
		print(symbols[len(symbols)-i+1], " ", end = '')
	for i in range(len(symbols)):
		print("( " +str(symbols[i].get_num_children())+ " ) ", end = '')
# n = [list of nodes, pattern] is list of nodes (list of 1 node, really)
# symbols is list of patterns

def generateOrderedString(n):
	s = ""
	for i in range(n):
		for j in range(5):
			if(i%2 == 0):
				s += str(1)
			else:
				s+=str(0)
	return s
def generateRandomString(n):
	s = ""
	for i in range(n*5):
		s+= str(np.random.randint(0,2))
	return s

if __name__ == '__main__':
	#string = "0100010101101"
	string = "01101101011101"
	string = generateOrderedString(10)
	string = generateRandomString(10)
	tcodes = t_code_it_up(string)

	compression = print_t_code_pattern(tcodes, string)
	print("\n \n \n here")

	complexity = compression[0]
	print("\nTCode Complexity =" + str(complexity) + " per bit: "+ str(complexity/len(string)))
	print("\n")
	print(" compression:\n ")
	size = ""
	print("dictionary: ",end = '')
	for i in range(len(compression[1][0])):
		size+= str(compression[1][0][i])
		print(str(compression[1][0][i]) +" ",end='')
	print("exponents:")
	for i in range(len(compression[1][1])):
		size+= str(bin(compression[1][1][i]))[2:]
		print("( " + str(compression[1][1][i]) +" ) ",end='')

	print("compression:")
	print(size)
	print(string)
	print("compression from ", end='')
	print(len(string), end = '')
	print(" to ", end = '')
	print(len(size))









