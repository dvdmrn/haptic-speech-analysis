import csv
import numpy as np
import itertools

"""
pID | vib_style | placement | accuracy
1      ctrl     hands       0.4
1      s1       hands       0.8
1      ctrl     neck        0.4
1      s1       neck        0.8
2      ctrl     hands       0.4
...

pID | vib_style | placement | accuracy | contrast
1     ctrl        hands       0.4        vf
1     ctrl        hands       0.8        vs
1     ctrl        hands       0.8        hlV
1     ctrl        neck        0.8        vf
1     ctrl        neck        0.8        vs
1     ctrl        neck        0.8        hlV
1     s1          hands       0.4        vf
1     s1          hands       0.8        vs
1     s1          hands       0.8        hlV
1     s1          neck        0.8        vf
1     s1          neck        0.8        vs
1     s1          neck        0.8        hlV
1     s2          hands       0.4        vf
1     s2          hands       0.8        vs
1     s2          hands       0.8        hlV
1     s2          neck        0.8        vf
1     s2          neck        0.8        vs
1     s2          neck        0.8        hlV



1     ctrl        neck        0.4
1     s1          neck        0.8
2     ctrl        hands       0.4
...



"""
def generateConditionSets():
	factor1 = ["hands","neck"]
	factor2 = ["amp","lowfi","ctrl"]
	factor3 = ["vf","vs","Vhl"]
	c=itertools.product(factor1,factor2,factor3)
	conditionSets = []
	for e in c:
		conditionSets.append(e)
	return conditionSets

conditionSets = generateConditionSets()


def getFieldScore(pID, reader):
	"""
	gets a field's average accuracy score
	"""

	newRows = [] # {"pID":x, "placement":x, "vib_style":x, "contrast":x, "accuracy":x}

	for s in conditionSets:
		condAverage = []
		for row in reader:
			if row['pID'] == pID and row['placement'] == s[0] and row['vib_style'] == s[1] and row['contrast'] == s[2]:
				condAverage.append(float(row['correct']))
		ave = np.average(condAverage)
		newRows.append({"pID":pID, "placement":s[0], "vib_style":s[1], "contrast":s[2], "accuracy":ave})

	return newRows


with open("master_output.csv","r") as csvfile:
	reader = csv.DictReader(csvfile)
	pIDs = []
	localReader = []
	master_output = []

	# populates localreader as an array of dicts
	for row in reader: localReader.append(row)


	for row in localReader:
		if row['pID'] not in pIDs:
			pIDs.append(row['pID'])

	for pID in pIDs:
		# need to get:
		# {pID:,vib_style:,placement:,accuracy}
		pscores = getFieldScore(pID,localReader)
		[master_output.append(s) for s in pscores]
	print(master_output)

with open("processed_data.csv","w") as csvfile:
	headers = ["pID","placement","vib_style","contrast","accuracy"]
	writer = csv.DictWriter(csvfile, fieldnames=headers)
	writer.writeheader()
	writer.writerows(master_output)

items = [{"pID":1,"b":2,"c":3},{"pID":1,"d":2,"c":4},{"pID":1,"b":2,"c":69},{"pID":222,"b":2,"c":3},{"pID":222,"b":2,"c":3},{"pID":222,"b":2,"c":63}]
c = itertools.product(items)
print c

for i in c: 
	for e in i:
		print e

