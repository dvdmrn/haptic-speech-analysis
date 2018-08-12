import csv

"""
removes postvocalic consonant contrasts from responses
"""

headers = ["response", "token", "correct", "contrast", "vib_style","placement","pID"]

def getMinPairMap():
	with open("minpairmap.csv","r") as csvfile:
		minpairmap = []
		reader = csv.DictReader(csvfile)
		for row in reader:
			minpairmap.append(row)

		return minpairmap

def removePostvocalic(targetCSV,minpairmap):
	print minpairmap
	purgedCSV = []
	for row in targetCSV:
		for minpair in minpairmap:
			if minpair["p0"] == row["token"] or minpair["p1"] == row["token"]:
				if minpair["postvocalic_consonant"] == "0":
					purgedCSV.append(row)
	return purgedCSV

def writeOut(writeMeDaddy):
	with open("no_postvocalic_consonants_out.csv","w") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=headers)
		writer.writeheader()
		writer.writerows(writeMeDaddy)


def main():
	minpairs = getMinPairMap()
	with open("master_output.csv","r") as csvfile:
		targetFile = []
		reader = csv.DictReader(csvfile)
		for row in reader:
			targetFile.append(row)
		purgedPostvocalics = removePostvocalic(targetFile,minpairs)
		writeOut(purgedPostvocalics)

main()