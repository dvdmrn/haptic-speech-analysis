import csv
import os
from numpy import average as ave 

OFFSETS = [300,200,100,50,0,-50,-100,-200,-300]

def openCSV(path):
	participantData = []
	with open(path) as responseSheet:
	        reader = csv.DictReader(responseSheet)
	        for row in reader:
	            participantData.append(row)
	return participantData

def aveForOffset(offset,participantData):
	correctResponses = []
	for row in participantData:
		# print("looking at : ",row["offset"])
		if row["offset"] == str(offset):
			correctResponses.append(float(row["correct"]))
	print(ave(correctResponses))

def main():
	print "in main"
	pdata = openCSV("data/55_minpair_responses.csv")

	for offset in OFFSETS:
		aveForOffset(offset,pdata)

main()