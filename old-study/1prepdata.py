import csv
import os
import re
import pprint
"""
even: neck first
odd: hands first

add rows for: neck, pid

"""

pp = pprint.PrettyPrinter(indent=2)


headers = ["response", "token", "correct", "contrast", "vib_style","placement","pID"]



def getFilesToProcess():
	files = [] # {path, pID}
	for d in os.walk('data'):
		for f in d[2]:
			if (".csv" in f) and not (".INVALID" in f):
				m = re.search(r'\d+', f)
				print("m: ",m)
				if m:
					pID = m.group(0)
					files.append({"path":os.path.join(d[0],f),"pID":pID})
				else:
					break
				# print("FOUND: ",m.group(0),f,d[0])
	pp.pprint(files)
	return files

files = getFilesToProcess()

master = [] # list of dicts

for f in files:

	with open(f['path'],'rb') as csvfile:
		rowIndex = 0
		print("opening... ",f['path'])
		currentFile = []
		reader = csv.DictReader(csvfile)
		placement = ""
		for row in reader:
			rowIndex += 1
			if int(f['pID']) % 2 == 0:
				if rowIndex <= 90:
					placement = "neck"
				else:
					placement = "hands"
			else:
				if rowIndex <= 90:
					placement = "hands"
				else:
					placement = "neck"

			row['pID'] = f['pID']
			row['placement'] = placement 
			master.append(row)
		pp.pprint(currentFile)

with open("master_output.csv","w") as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=headers)
	writer.writeheader()
	writer.writerows(master)