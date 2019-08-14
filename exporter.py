#AETEX EXPORTER
#pseudocode: write the following:
#01, 00x3, 05, 00x3, 4a, 00 ,e1, 00, 02 ,00x3, 03, 00x03,
#4 BYTES: WIDTH (byte order reversed)
#4 bytes: height
#30, 00x3, 01, 00x15, 38, 00x3, 12, 00, e1, 00x3, 02, 00x10, 0a, a0, 05, 20, 20

cnstBytes = bytearray([0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00])
cnstBytes1andahalf = bytearray([0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00])
cnstBytes2 = bytearray([0x30, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x12, 0x40, 0x38, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0xd0, 0x02, 0x20, 0x20])

import numpy as np
import cv2
from tkinter import filedialog

img = cv2.imread(filedialog.askopenfile(filetypes=[('PNG images', '.png'), ('JPEG images', '.jpg'), ('all files', '.*')]).name, cv2.IMREAD_UNCHANGED)
height, width, channels = img.shape

saveas = filedialog.asksaveasfile(mode='w', defaultextension=".aetex")
saveasFile = open(saveas.name, "w+b")
saveasFile.write(cnstBytes)

fileSize = ((height*width * 4) + 0x4a).to_bytes(4, byteorder="big")
saveasFile.write(bytearray((fileSize[3], fileSize[2], fileSize[1], fileSize[0])))
saveasFile.write(cnstBytes1andahalf)

w23 = width.to_bytes(4, byteorder="big")
width2 = (w23[3], w23[2], w23[1], w23[0])
saveasFile.write(bytearray(width2))

h23 = height.to_bytes(4, byteorder="big")
height2 = (h23[3], h23[2], h23[1], h23[0])
saveasFile.write(bytearray(height2))

saveasFile.write(cnstBytes2)

for x in img:
	for y in x:
		saveasFile.write(bytearray(y))