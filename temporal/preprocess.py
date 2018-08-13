import csv
import os
from numpy import average as ave 
import re
import pprint as pp

OFFSETS = [300,200,100,50,0,-50,-100,-200,-300]

'''
creates a csv containing all average participant acc scores in the format:

participant_ID | accuracy | offset
1              | 0.5      | -300
1              | 0.6      | -200
...
2              | 0.55     | -300
2              | 0.56     | -200
...
n              | 0.4      | -300

'''



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
	return ave(correctResponses)

def writeCSV(path,rows):
	print "----------------------\nwriting CSV: "+path
	fieldNames = ["pID","offset","accuracy"]
	with open(path,"w") as csvFile:
		writer = csv.DictWriter(csvFile,fieldnames=fieldNames)
		writer.writeheader()
		writer.writerows(rows)



def getFilesToProcess():
	files = [] # {path, pID}
	for d in os.walk('data'):
		for f in d[2]:
			if (".csv" in f) and not (".INVALID" in f):
				m = re.search(r'\d+', f)
				if m:
					pID = m.group(0)
					files.append({"path":os.path.join(d[0],f),"pID":pID})
				else:
					break
				# print("FOUND: ",m.group(0),f,d[0])
	print "FOUND FILES:"
	pp.pprint(files)
	return files

def main():
	files = getFilesToProcess()
	csvData = []
	for f in files:
		pdata = openCSV(f["path"])
		print "PARTICIPANT "+f["pID"]+" ----------------------"
		for offset in OFFSETS:
			ave = aveForOffset(offset,pdata)
			print(offset,ave)
			rowToWrite = {"pID":f["pID"],"offset":str(offset),"accuracy":ave}
			csvData.append(rowToWrite)
	writeCSV("temporal_offset_scores.csv",csvData)
	print "----------------------\ncomplete!"

main()