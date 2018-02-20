import numpy as np

s = "asdadasdasdasdasdasdasdasaasasadaad"

class LZ77:
	s = ""
	p = 0 # current position
	compression = [] # this will be a linked list of ordered triples (distance back, length, added char)

	def __init__(string):
		s = string

	def compress():
		for i in range(len(s)):
			for j in range(i):
				