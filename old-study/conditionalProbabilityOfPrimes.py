import csv
import numpy as np 
import prepdata 
import pprint
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon

"""
gets the conditional probability of p(the first 5 items are correct | first stimuli was of type X)

code's spaghetti, look away
"""
pp = pprint.PrettyPrinter(indent=2)

localReader = []
conditionSets = [] # [{'prime':'vib_style','accuracy':0.0}, ...]
unconditionalProbabilities = {"amp":[],"lowfi":[],"ctrl":[]}
conditionalProbabilities = {"amp":[],"lowfi":[],"ctrl":[]}
GUP = {"amp":[],"lowfi":[],"ctrl":[]} # global unconditional probabilities

def getCSV(path):
	csvData = []
	with open(path,"r") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			csvData.append(row)
		return csvData



def getConditionalProbability(data):
	global conditionSets
	accuracyScores = []

	for i in range(0,5):
		if i==0:
			firstStyle = data[i]['vib_style']
		accuracyScores.append(int(data[i]['correct']))
	aveAcc = np.average(accuracyScores)
	conditionSets.append({"prime":firstStyle,"accuracy":aveAcc})

def chewThroughFiles():
	for f in prepdata.files:
		data = getCSV(f["path"])
		getConditionalProbability(data)
		unconditionalProbabilityOfPrimes(data[0])


def getGlobalUnconditionalProbabilities():
	global GUP
	for f in prepdata.files:
		data = getCSV(f["path"])

		for row in data:
			if row['vib_style'] == 'ctrl':
				GUP['ctrl'].append(float(row['correct']))
			if row['vib_style'] == 'amp':
				GUP['amp'].append(float(row['correct']))
			if row['vib_style'] == 'lowfi':
				GUP['lowfi'].append(float(row['correct']))

	c=np.average(GUP['ctrl'])
	a=np.average(GUP['amp'])
	l=np.average(GUP['lowfi'])
	
	print("p(ctrl)",np.average(GUP['ctrl']))
	print("p(amp)",np.average(GUP['amp']))
	print("p(lowfi)",np.average(GUP['lowfi']))

	return {"ctrl":c,"amp":a,"lowfi":l}

def sortBuckets():
	global conditionalProbabilities
	ctrlVals = []
	ampVals = []
	lowfiVals = []
	for s in conditionSets:
		if s['prime'] == 'ctrl':
			ctrlVals.append(s['accuracy'])
		if s['prime'] == 'amp':
			ampVals.append(s['accuracy'])
		if s['prime'] == 'lowfi':
			lowfiVals.append(s['accuracy'])

	conditionalProbabilities['ctrl'] = ctrlVals
	conditionalProbabilities['amp'] = ampVals
	conditionalProbabilities['lowfi'] = lowfiVals
	aveCtrl = np.average(ctrlVals)
	aveAmp = np.average(ampVals)
	aveLowfi = np.average(lowfiVals)

	return [{"condition":"p(correct|ctrl)","value":aveCtrl},{"condition":"p(correct|amp)","value":aveAmp},{"condition":"p(correct|lowfi)","value":aveLowfi}]


def unconditionalProbabilityOfPrimes(row):
	global unconditionalProbabilities
	if row['vib_style'] == 'ctrl':
		unconditionalProbabilities['ctrl'].append(float(row['correct']))
	if row['vib_style'] == 'amp':
		unconditionalProbabilities['amp'].append(float(row['correct']))
	if row['vib_style'] == 'lowfi':
		unconditionalProbabilities['lowfi'].append(float(row['correct']))

def calcUnconditionalProbability():
	global unconditionalProbabilities
	ctrl = np.average(unconditionalProbabilities['ctrl'])
	amp = np.average(unconditionalProbabilities['amp'])
	lowfi = np.average(unconditionalProbabilities['lowfi'])
	print("UNCONDITIONAL PROBABILITIES: \n"+"    ctrl: "+str(ctrl)+" | amp: "+str(amp)+" | lowfi: "+str(lowfi))


def main():
	chewThroughFiles()
	results = sortBuckets()
	pp.pprint(results)
	calcUnconditionalProbability()
	ctrlttest = ttest_rel(conditionalProbabilities['ctrl'],unconditionalProbabilities['ctrl'])
	ampttest = ttest_rel(conditionalProbabilities['amp'],unconditionalProbabilities['amp'])
	lowfittest = ttest_rel(conditionalProbabilities['lowfi'],unconditionalProbabilities['lowfi'])
	

	print("length of ctrl: ",len(unconditionalProbabilities['ctrl']))
	print("length of amp: ",len(unconditionalProbabilities['amp']))
	print("length of lowfi: ",len(unconditionalProbabilities['lowfi']))

	print("len of cond ctrl: ",len(conditionalProbabilities['ctrl']))
	print("len of cond amp: ",len(conditionalProbabilities['amp']))
	print("len of cond lowfi: ",len(conditionalProbabilities['lowfi']))

	print("\nctrl: ",ctrlttest,"\namp: ",ampttest,"\nlowfi: ",lowfittest)

	uncondProbs = getGlobalUnconditionalProbabilities()

	# ctrlttest2 = wilcoxon(conditionalProbabilities['ctrl'],GUP['ctrl'])
	# ampttest2 = wilcoxon(conditionalProbabilities['amp'],GUP['amp'])
	# lowfittest2 = wilcoxon(conditionalProbabilities['lowfi'],GUP['lowfi'])
	# print('ctrl cond x global uncond: ',ctrlttest2)
	# print('amp cond x global uncond: ',ampttest2)
	# print('lowfi cond x global uncond: ',lowfittest2)


main()