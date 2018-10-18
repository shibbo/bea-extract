import struct

class EndianBinaryReader:

	data = None
	offset = 0
	isLittleEndian = True
	filepath = None
	
	def __init__(self, filepath, endian):
		self.filepath = filepath
		self.isLitleEndian = endian
		self.offset = 0
		
	def open(self):
		print(f"Opening file {self.filepath}...")
		
		with open(self.filepath, 'rb') as f:
			self.data = f.read()
			
		if self.data is None:
			raise ValueError("Data is none, is this an empty file?")
			
	def seek(self, pos):
		self.offset = pos
		
	def readU8(self):
		ret, = struct.unpack_from("B", self.data, self.offset)
		self.offset += 1
		return ret
		
	def readU16(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}H", self.data, self.offset)
		self.offset += 2
		return ret
		
	def readU32(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}I", self.data, self.offset)
		self.offset += 4
		return ret
		
	def readU64(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}L", self.data, self.offset)
		self.offset += 8
		return ret
		
	def readS8(self):
		ret, = struct.unpack_from("b", self.data, self.offset)
		self.offset += 1
		return ret
		
	def readS16(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}h", self.data, self.offset)
		self.offset += 2
		return ret
		
	def readS32(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}i", self.data, self.offset)
		self.offset += 4
		return ret
		
	def readS64(self):
		if self.isLittleEndian:
			endian = '<'
		else:
			endian = '>'

		ret, = struct.unpack_from(f"{endian}l", self.data, self.offset)
		self.offset += 8
		return ret
		
	def readU8RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readU8()
		seek(curPos)
		return ret
		
	def readU16RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readU16()
		seek(curPos)
		return ret
		
	def readU32RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readU32()
		seek(curPos)
		return ret
		
	def readU64RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readU64()
		seek(curPos)
		return ret
		
	def readS8RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readS8()
		seek(curPos)
		return ret
		
	def readS16RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readS16()
		seek(curPos)
		return ret
		
	def readS32RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readS32()
		seek(curPos)
		return ret
	
	def readS64RelativeOffset(self):
		curPos = self.offset + 4
		seek(readU32())
		ret = readS64()
		seek(curPos)
		return ret
		
	def readString(self, len=0):
		if len == 0:
			end = self.data.find(b'\0', self.offset)
			return data[offset:end].decode('latin-1')
			
		ret, = struct.unpack_from(f"{len}s", self.data, self.offset)
		self.offset += len
		return ret
		
	def readStringAtOffsetWithLength(self, offset):
		curPos = self.offset + 8
		self.seek(offset)
		length = self.readU16()
		ret, = struct.unpack_from(f"{length}s", self.data, self.offset)
		self.seek(curPos)
		return ret
		
	def readDataAtOffset(self, offset, len):
		return self.data[offset:offset+len]	
		
	def readPad(self, numBytes=1):
		self.offset += numBytes