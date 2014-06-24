import PIL
from PIL import Image
import ImageFont, ImageDraw
import collections
from collections import Counter
import math
import random

def makeAChart(data):
	CommandPrompt12x16 = ImageFont.truetype('Command-Prompt-12x16.ttf',32)
	minimumColorValue=64
	topOfDomain=635
	minimumDatum = min(data)
	maximumDatum = max(data)
	domain = Image.open('domain.PNG')
	display= Image.open('display.PNG')
	bands = []
	for datum in range(len(data)):
		point = int(((data[datum]-minimumDatum)/float((maximumDatum-minimumDatum)))*900)
		bands+=[point]
	overlaps=0
	previous=0
	for point in bands:
		if (point-previous)<6:
			overlaps+=1
			previous=0
			previous+=point
	print 'OVERLAPS', overlaps
	singleGradient = int(192. / overlaps)
	chart=Image.new('RGB',(1200,800),(0,0,0))
	for point in bands:
		for sides in range(3):
			curR,curG,curB = chart.getpixel((point+sides+150,topOfDomain))
			if curR==0:
				newCol = minimumColorValue	
			elif (curR+singleGradient)>255:
				newCol = 255
			else:
				newCol=curR+singleGradient
			for above in range(100):
				chart.putpixel((point+150+sides,topOfDomain+above),(newCol,newCol,newCol))
			curR,curG,curB = chart.getpixel((point-sides+150,topOfDomain+above))
			if curR==0:
				newCol = minimumColorValue	
			elif (curR+singleGradient)>255:
				newCol = 255
			else:
				newCol=curR+singleGradient
			for above in range(100):
				chart.putpixel((point+150-sides,topOfDomain+above),(newCol,newCol,newCol))
	chart.paste(domain,(150,topOfDomain+105))
	chart.paste(display,(0,0))
	texting = ImageDraw.Draw(chart)
	texting.text((150-len(str(minimumDatum))*12,topOfDomain+120),str(minimumDatum),font=CommandPrompt12x16,fill=(192,192,192))
	texting.text((1050-len(str(maximumDatum))*12,topOfDomain+120),str(maximumDatum),font=CommandPrompt12x16,fill=(192,192,192))	
	texting.text((600-len(str(((maximumDatum-minimumDatum)/2.)+minimumDatum))*12,topOfDomain+120),str(((maximumDatum-minimumDatum)/2.)+minimumDatum),font=CommandPrompt12x16,fill=(192,192,192))	
	chart.show()
	chart.save('CHART.PNG','png')