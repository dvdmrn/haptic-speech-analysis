import csv
import os
from numpy import average as ave 
import re
import pprint as pp

HEADERS = ["pID", "correct", "token", "vib_style", "offset", "response", "contrast"]
NARROW = True
masterData = []

'''
creates a csv containing all average participant acc scores in the format:

'''



def openCSV(path):
    print("path: ",path)
    m = re.search(r'\d+', path)
    print(m.group(0))
    participantData = []
    with open(path) as responseSheet:
        reader = csv.DictReader(responseSheet)
        print(reader)
    # for row in reader:
    #     print("hello")
        for row in reader:
            print("help")
            row["pID"] = m.group(0)
            participantData.append(row)
   	
    return participantData


def writeCSV(path,rows):
	print "----------------------\nwriting CSV: "+path
	fieldNames = HEADERS
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
	contrasts = ["vf","vs","Vhl"]
	for f in files:
		pdata = openCSV(f["path"])
		print "PARTICIPANT "+f["pID"]+" ----------------------"
		for row in pdata:
			masterData.append(row)

	print("MASTER DATA: ",masterData)

	writeCSV("MASTER_TEMPORAL_DATA.csv",masterData)
	# print "----------------------\ncomplete!"

main()