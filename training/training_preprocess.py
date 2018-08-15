import csv
import os
from numpy import average as ave 
import re
import pprint as pp


'''
creates a csv containing all average participant acc scores in the format:

participant_ID | accuracy | cond
1              | 0.5      | ctrl
1              | 0.6      | amp
...
2              | 0.55     | -300
2              | 0.56     | -200
...
n              | 0.4      | -300

'''

NARROW = True

def openCSV(path):
	participantData = []
	with open(path) as responseSheet:
	        reader = csv.DictReader(responseSheet)
	        for row in reader:
	            participantData.append(row)
	return participantData

def aveForCond(cond,participantData):
	correctResponses = []
	for row in participantData:
		# print("looking at : ",row["offset"])
		if row["vib_style"] == str(cond):
			correctResponses.append(float(row["correct"]))
	return ave(correctResponses)

def aveForCondAndContrast(contrast, cond,participantData):
	correctResponses = []
	for row in participantData:
		if (row["contrast"] == contrast) and (row["vib_style"] == str(cond)):
			correctResponses.append(float(row["correct"]))
	return ave(correctResponses)



def writeCSV(path,rows):
	print "----------------------\nwriting CSV: "+path
	if NARROW:
		fieldNames = ["pID","cond","accuracy","contrast"]
	else:
		fieldNames = ["pID","cond","accuracy"]
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
		for cond in ["ctrl","amp"]:
			if not NARROW:
				# net averages for erryone
				ave = aveForCond(cond,pdata)
				print(cond,ave)
				rowToWrite = {"pID":f["pID"],"cond":str(cond),"accuracy":ave}
				csvData.append(rowToWrite)
			else:
				# averages for condition x contrast
				contrasts = ["vf","vs","Vhl"]
				for contrast in contrasts:
					ave = aveForCondAndContrast(contrast,cond,pdata)
					print(contrast,cond,ave)
					rowToWrite = {"pID":f["pID"],"cond":str(cond),"accuracy":ave,"contrast":contrast}
					csvData.append(rowToWrite)

	writeCSV("training_scores.csv",csvData)
	print "----------------------\ncomplete!"

main()