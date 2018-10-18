import reader

class Node:
	reference = 0
	indexLeft = 0
	indexRight = 0
	keyOffset = 0
	key = None
	reader = None
	
	def __init__(self, r):
		self.reader = r
		
	def parseData(self):
		self.reference = self.reader.readU32()
		self.indexLeft = self.reader.readU16()
		self.indexRight = self.reader.readU16()
		self.keyOffset = self.reader.readS64()
		
		self.key = self.reader.readStringAtOffsetWithLength(self.keyOffset)
		
		print(f"\tDictionary Node Found\n\tReference: {self.reference}\n\tIndex Left: {self.indexLeft}\n\tIndex Right: {self.indexRight}\n\tKey Offset: {hex(self.keyOffset)}\n\tKey: {self.key}")


class DICT:
	reader = None
	magic = None
	nodeCount = 0
	
	nodes = []

	def __init__(self, reader):
		self.reader = reader
		
	def parseData(self, offset):
		self.reader.seek(offset)
		self.magic = self.reader.readString(0x4)
		self.nodeCount = self.reader.readU32()
		
		baseAddr = self.reader.offset
		
		for i in range(self.nodeCount):
			self.reader.seek(baseAddr + (0x30 * i))
			node = Node(self.reader)
			node.parseData()
			self.nodes.append(node)