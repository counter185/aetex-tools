from io import FileIO
import sys
import os
import traceback

sampleDDSDXT1Header = bytes([
    0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x07, 0x10, 0x08, 0x00, 0xFF, 0xFF, 0x00, 0x00, 
    0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 
    0x04, 0x00, 0x00, 0x00, 0x44, 0x58, 0x54, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
])

sampleDDSDXT3Header = bytes([
    0x44, 0x44, 0x53, 0x20, 0x7C, 0x00, 0x00, 0x00, 0x07, 0x10, 0x08, 0x00, 0xFF, 0xFF, 0x00, 0x00, 
    0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 
    0x04, 0x00, 0x00, 0x00, 0x44, 0x58, 0x54, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
])

def positionInFileBounds(file: FileIO, pos: int) -> bool:
    return pos >= 0 and pos < os.fstat(file.fileno()).st_size

def readInt32(file: FileIO) -> int:
    return int.from_bytes(file.read(4), 'little')
def writeInt32(file: FileIO, value: int):
    file.write(int.to_bytes(value, 4, 'little'))

def readInt16(file: FileIO) -> int:
    return int.from_bytes(file.read(2), 'little')

def readInt8(file: FileIO) -> int:
    return int.from_bytes(file.read(1), 'little')

def copyAllBytesToNewFile(file: FileIO, name: str):
    outfile = open(name, 'wb')
    outfile.write(file.read())
    outfile.close()
    print(f" -> {name}")

def copyAllBytesToFile(file: FileIO, outfile: FileIO):
    outfile.write(file.read())

def writeBytesToFile(file: FileIO, data: bytes):
    file.write(data)

files = sys.argv[1:] if len(sys.argv) > 1 else [input("File name>")]
for filename in files:
    if filename.endswith(".aetex"):
        try:
            infile = open(filename, 'rb')

            magicNumber = readInt16(infile)

            infile.seek(0x04)
            gameType = readInt8(infile)

            infile.seek(0x08)
            b08 = readInt8(infile)

            infile.seek(0x0C)
            r2compressionMethod = readInt8(infile)

            infile.seek(0x10)
            imgW = readInt16(infile)
            imgH = readInt16(infile)

            infile.seek(0x2C)
            r2DataStart = readInt32(infile)

            if gameType == 0x0a:
                infile.seek(r2DataStart)
                ddsheader = infile.read(3)

                infile.seek(0x28)
                gxtHeaderPos = readInt32(infile)
                if positionInFileBounds(infile, gxtHeaderPos):
                    infile.seek(gxtHeaderPos)
                    gxtheader = infile.read(3)
                infile.seek(r2DataStart)
                
                if ddsheader[0] == 0x44 and ddsheader[1] == 0x44 and ddsheader[2] == 0x53:
                    copyAllBytesToNewFile(infile, filename.replace(".aetex", ".dds"))
                elif gxtheader[0] == 0x47 and gxtheader[1] == 0x58 and gxtheader[2] == 0x54:
                    infile.seek(gxtHeaderPos)
                    copyAllBytesToNewFile(infile, filename.replace(".aetex", ".gxt"))
                elif r2compressionMethod == 0x8B:
                    #dxt1
                    name = filename.replace(".aetex", ".dds")
                    outfile = open(name, 'wb')
                    writeBytesToFile(outfile, sampleDDSDXT1Header)
                    outfile.seek(0x0C)
                    writeInt32(outfile, imgH)
                    writeInt32(outfile, imgW)
                    writeInt32(outfile, imgW * 2)
                    outfile.seek(0, os.SEEK_END)
                    copyAllBytesToFile(infile, outfile)
                    print(f" -> {name}")
                elif r2compressionMethod == 0x8C:
                    #dxt2/3
                    name = filename.replace(".aetex", ".dds")
                    outfile = open(name, 'wb')
                    writeBytesToFile(outfile, sampleDDSDXT3Header)
                    outfile.seek(0x0C)
                    writeInt32(outfile, imgH)
                    writeInt32(outfile, imgW)
                    writeInt32(outfile, imgW * 4)
                    outfile.seek(0, os.SEEK_END)
                    copyAllBytesToFile(infile, outfile)
                    print(f" -> {name}")
                    pass
                elif r2compressionMethod == 0x81:
                    infile.seek(r2DataStart)
                    copyAllBytesToNewFile(infile, filename.replace(".aetex", ".tga"))
            elif b08 == 0x80:
                infile.seek(0x80)
                #todo: add a proper astc header
                copyAllBytesToNewFile(infile, filename.replace(".aetex", ".astc"))
            else:
                infile.seek(0x38)
                copyAllBytesToNewFile(infile, filename.replace(".aetex", ".tga"))
        except Exception as e:
            traceback.print_exception(e)
