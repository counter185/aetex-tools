from io import FileIO
import sys
import os

def readInt(file: FileIO) -> int:
    return int.from_bytes(file.read(4), 'little')

def decomp(filename: str):
    shaderfile = open(filename, 'rb')
        
    unk1 = readInt(shaderfile)
    unk2 = readInt(shaderfile)
    wholeFileSize = readInt(shaderfile)
    shaderStartOffset = readInt(shaderfile)
    shaderCodeLength = readInt(shaderfile)

    shaderfile.seek(shaderStartOffset)

    outputshader = open(filename.replace(".aeshader", ".fx"), 'wb')
    outputshader.write(shaderfile.read(shaderCodeLength-1))
    outputshader.close()

def compile(filename:str):
    outfile: FileIO = open(filename.replace(".fx", ".aeshader"), 'wb')
    infile: FileIO = open(filename, 'rb')
    infilesize: int = os.stat(filename).st_size
    outfile.write(int.to_bytes(0x0C, 4, 'little'))
    outfile.write(int.to_bytes(0x04, 4, 'little'))
    outfile.write(int.to_bytes(0x5C+infilesize+1, 4, 'little'))
    outfile.write(int.to_bytes(0x5C, 4, 'little'))
    outfile.write(int.to_bytes(infilesize+1, 4, 'little'))
    outfile.write(bytes("vs_main", 'ascii'))
    for x in range(0x19):
        outfile.write(b'\x00')
    for x in range(0x8):
        outfile.write(b'\xCD')
    outfile.write(bytes("ps_main", 'ascii'))
    outfile.write(b'\x00')
    for x in range(0x18):
        outfile.write(b'\xCD')
    outfile.write(infile.read(infilesize))
    outfile.write(b'\x00')

filename: str = input() if len(sys.argv) < 2 else sys.argv[1]
if filename.endswith(".fx"):
    compile(filename)
else:
    decomp(filename)
