#!/usr/bin/env python
from PIL import Image
import sys
## TODO: Make a GUI version of this.. and for the CLI version make a cool progress bar

## Gets user input for location of image and size of desired pixelation
## Resizes image to ensure no rectangle pixels occur 
def main():
	if (len(sys.argv) - 1) < 2:
		print "ERROR! too few arguments... type 'pixeler -h' for help"
		return
	elif (len(sys.argv) - 1) > 2:
		print "ERROR! Too many arguments ... type 'pixeler -h' for help"
		return
	elif sys.argv[1] == "-h":
		print "Usage: pixeler [image file] [pixel size]" 
		return
	elif (not sys.argv[2].isdigit()):
		print "ERROR! Pixel size is not an integer" 
		return
	else:
		picLocation = sys.argv[1]
		pixSize = int(sys.argv[2])

	try: 
		picture = Image.open(picLocation)
	except IOError:
		print "ERROR! Image not found"
		return

        if picture.format != "JPEG" or picture.format != "JPG":
            picture = picture.convert('RGB')

	picW , picH = picture.size
	picture = picture.resize((((picW / pixSize) * pixSize) , ((picH / pixSize) * pixSize)))
	
	picture = pixelize(picture, pixSize)
	picture.save('pixelized.jpg')

## Access the picture a pixel * pixel size block at a time, getting average RGB values
## and applying the pixelization of average RGB values
def pixelize(pic, pixel):
	for i in range(0, (pic.size)[1], pixel):
		for j in range(0, (pic.size)[0], pixel):
			(avgR, avgG, avgB) = getPixelAverage(pic.crop((j, i, j + pixel, i + pixel)), pixel)
			pic = applyPixel(pic, avgR, avgG, avgB, i, j, pixel) 		
	return pic

## Gets the average RGB values from each block from pixelize 
def getPixelAverage(subPic, pix):
	r, g, b = (0, 0, 0)
	
	for i in range(0, pix, 1):
		for j in range(0, pix, 1):
			pixel = subPic.getpixel((i,j))
			r += pixel[0]
			g += pixel[1]
			b += pixel[2]
	
	r /= (pix * pix)
	g /= (pix * pix)
	b /= (pix * pix)

	return (r, g, b) 		

## Where the magic happens bb ;) 
def applyPixel(fullPic, r, g, b, y, x, pixSize):
	for i in range(0, pixSize, 1):
		for j in range(0, pixSize, 1):
			fullPic.putpixel(((x+i), (y+j)), (r, g, b))
	return fullPic
	
main()
	
	
