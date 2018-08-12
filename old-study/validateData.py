import csv
import numpy as np

"""
This is mainly done because it looks like we were missing a data point
for amp x vHL, given that it looks like a straight line,
but it looks like it's just a coincidence...
"""

path = "processed_data_full.csv"

targetValues = []

with open(path,'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['vib_style'] == "amp" and row['contrast'] == 'Vhl':
				targetValues.append(float(row['accuracy']))

result = np.average(targetValues)
print(result)