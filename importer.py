from tkinter import filedialog
import cv2
import os
import numpy as np
import math

#Variable explanation:
#a: input file path
#inpFile: input file
#fileSize: well, uhhh... input file size
#fileStart: location of the start of input file's graphics data
#imageX, imageY: image width and height, 4 bytes, but reversed, for example 512 (00 00 02 00) would be 00 02 00 00
#imageX1, 2, 3, 4, imageY1, 2, 3, 4: these exist to reorder bytes in image width and height
#imageXInt, imageYInt: the above, but as a normal int
#programCounterX, programCounterY: current X and Y positions, used in the image reading loop
#programCounterXMax, programCounterYMax: maximum values for programCounterX and programCounterY
#newImage: output image
#r, g, b, a: red, green, blue and alpha values for the currently read pixel

a = filedialog.askopenfile(filetypes=[('all files', '.*'), ('AETEX files', '.aetex')]).name

inpFile = open(a, "rb")
fileSize = os.path.getsize(a)
print("File size: " + str(fileSize))
inpFile.read(9)
#fileStart = int.from_bytes(inpFile.read(1), "big")				#TODO: find out where the graphics data actually starts, pretty sure it's not always 74/4A
fileStart = 74
print("graphics data start: " + str(fileStart))
#inpFile.read(fileStart - 9)

inpFile.read(11)
imageX1 = inpFile.read(1)
imageX2 = inpFile.read(1)
imageX3 = inpFile.read(1)
imageX4 = inpFile.read(1)

imageX = imageX4 + imageX3 + imageX2 + imageX1
imageYInt = int.from_bytes(imageX, "big")


imageY1 = inpFile.read(1)
imageY2 = inpFile.read(1)
imageY3 = inpFile.read(1)
imageY4 = inpFile.read(1)
imageY = imageY4 + imageY3 + imageY2 + imageY1
imageXInt = int.from_bytes(imageY, "big")

print("imageX: " + str(imageXInt))
print("imageY: " + str(imageYInt))

inpFile.read(fileStart - (8 + 11 + 4 + 5))

programCounterX = 0
programCounterXMax = imageYInt
programCounterY = 0
programCounterYMax = imageXInt

print("MaxX Program counter: " + str(programCounterXMax))
print("MaxY Program counter: " + str(programCounterYMax))

newImage = np.zeros((programCounterYMax, programCounterXMax, 4), np.uint8)

while programCounterY != programCounterYMax:
	r = int.from_bytes(inpFile.read(1), "big")
	g = int.from_bytes(inpFile.read(1), "big")
	b = int.from_bytes(inpFile.read(1), "big")
	a = int.from_bytes(inpFile.read(1), "big")
	#print("R: " + str(r) + " G: " + str(g) + " B: " + str(b))						#DEBUG: Only use if you need to, this slows down the program a lot
	newImage[programCounterY, programCounterX] = [r, g, b, a]
	#print("XPos: " + str(programCounterX) + " YPos: " + str(programCounterY))		#same here
	programCounterX += 1
	if programCounterX == programCounterXMax:
		programCounterX = 0
		programCounterY += 1

cv2.imshow("output", newImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Save? [Y/N]")
if input(">") == "Y":
	cv2.imwrite(filedialog.asksaveasfile(mode='w', filetypes=[("PNG images", ".png")], defaultextension=".png").name, newImage)