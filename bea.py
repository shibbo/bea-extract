import asst, dic, reader, sys

class BEA:

	reader = None
	magic = None
	version = 0
	byteOrder = 0
	alignment = 0
	targetAddrSize = 0
	assetBlockOffset = 0
	relocTableOffset = 0
	fileSize = 0
	fileCount = 0
	fileInfoOffset = 0
	dictOffset = 0
	unk = 0
	nameOffset = 0
	
	dict = None
	
	asstOffsets = []
	assets = []

	def __init__(self, r):
		self.reader = r

	def readHeader(self, doDump):
		self.magic = self.reader.readString(0x4)
		self.reader.readPad(0x4)
		self.version = self.reader.readU32()
		self.byteOrder = self.reader.readU16()
		self.alignment = self.reader.readU8()
		self.targetAddrSize = self.reader.readU8()
		self.reader.readPad(0x6)
		self.assetBlockOffset = self.reader.readU16()
		self.relocTableOffset = self.reader.readU32()
		self.fileSize = self.reader.readU32()
		self.fileCount = self.reader.readU64()
		self.fileInfoOffset = self.reader.readU64()
		self.dictOffset = self.reader.readU64()
		self.unk = self.reader.readU64()
		self.nameOffset = self.reader.readU64()
		
		# save our current position so we can resume reading the assets and all
		curPos = self.reader.offset
		
		dict = dic.DICT(self.reader)
		dict.parseData(self.dictOffset)
		
		self.reader.seek(curPos)
		
		for i in range (self.fileCount):
			self.asstOffsets.append(self.reader.readU64())
		
		print(f" Magic: {str(self.magic)}\n Version: {self.version}\n Byte Order: {self.byteOrder}\n Alignment: {self.alignment}\n Target Address Size: {self.targetAddrSize}\n Asset Block Offset: {hex(self.assetBlockOffset)}\n Relocation Table Offset: {hex(self.relocTableOffset)}\n File Size: {hex(self.fileSize)}\n File Count: {self.fileCount}\n File Info Offset: {hex(self.fileInfoOffset)}\n Dictionary Offset: {hex(self.dictOffset)}\n Unknown: {self.unk}\n Name Offset: {hex(self.nameOffset)}\n")
		
		print(f" File Name: {str(self.reader.readStringAtOffsetWithLength(self.nameOffset))}")
		
		print("==============================================")
		
		# go through every asset
		for offset in self.asstOffsets:
			self.reader.seek(offset)
			asset = asst.ASST(self.reader)
			asset.parseData(doDump)
			self.assets.append(asset)
			
		print("==============================================")
		
		
	def getAssetByName(self, name):
		for asset in self.assets:
			if asset.fileName == name:
				return asset
		
		return None
		
def main():
	if len(sys.argv) < 2:
		print("Syntax: python bea.py in.bea <options>\n-x Extract")
		sys.exit()
		
	r = reader.EndianBinaryReader(sys.argv[1], True)
	r.open()
	
	bea = BEA(r)
		
	if "-x" in sys.argv:
		bea.readHeader(True)
	else:
		bea.readHeader(False)
main()

print("Done!")