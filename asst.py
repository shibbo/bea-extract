import reader, os
import zstandard as zstd

class ASST:
	
	reader = None
	magic = None
	blockSize = 0
	unk1 = 0
	unk2 = 0
	fileSize = 0
	uncompressedSize = 0
	fileOffset = 0
	nameOffset = 0
	fileName = None
	compressedData = []
	uncompressedData = []

	def __init__(self, r):
		self.reader = r
		
	def parseData(self, doDump):
		self.magic = self.reader.readString(0x4)
		self.reader.readPad(0x4)
		self.blockSize = self.reader.readU64()
		self.unk1 = self.reader.readU16()
		self.unk2 = self.reader.readU16()
		self.fileSize = self.reader.readU32()
		self.uncompressedSize = self.reader.readS64()
		self.fileOffset = self.reader.readS64()
		self.nameOffset = self.reader.readS64()
		
		self.fileName = self.reader.readStringAtOffsetWithLength(self.nameOffset)
		
		print(f"\tAsset Found: {self.magic}\n\tBlock Size: {self.blockSize}\n\tUnknown 1: {self.unk1}\n\tUnknown 2: {self.unk2}\n\tFile Size: {hex(self.fileSize)}\n\tUncompressed Size: {hex(self.uncompressedSize)}\n\tFile Offset: {hex(self.fileOffset)}\n\tName Offset: {hex(self.nameOffset)}\n\tFile Name: {self.fileName}")
		
		compressedData = self.reader.readDataAtOffset(self.fileOffset, self.fileSize)
		
		uncompressedData = zstd.ZstdDecompressor().decompress(compressedData)
		
		if doDump:
			try:
				os.makedirs(os.path.dirname(self.fileName))
			except FileExistsError:
				pass
			
			with open(self.fileName, "wb") as f:
				f.write(uncompressedData)