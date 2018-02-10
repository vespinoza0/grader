import csv
import tkinter
from tkinter import filedialog
import os
import datetime
import config

myTAlist = config.TAlist
avgDict = []
b = ['Assignment','AvgScore','Sub_Rate', 'Sub_Avg']
avgDict.append(b)
#### Get a single Canvas CSV file to update! #############
print("##################################################################################################################")
print("Welcome to grader.py!!")
print("Please Select Canvas CSV file")
root = tkinter.Tk()
root.withdraw()
Ca = filedialog.askopenfilename(title = "Select canvas file",filetypes = (("CSV files","*.csv"),("all files","*.*")))  # get directory +filename.csv
head, tail = os.path.split(Ca)
print("You are now editing canvas file: ",tail)
with open(Ca) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	Can = list( csv.reader(csvDataFile))
total_students = len(Can)-3
Canheader = Can[0]
print("for all ", total_students , " students! Hope this code works!")
###############################################################


### this function gets the unique TU emai and inserts in the second column of the HR list
def modHR(Hr):
	email = []
	for row in range(1, len(Hr)):
		loginID =Hr[row][2]
		Hr[row].insert(17, loginID)
		loginID = loginID.lower()
		if loginID == config.loginID1:
			loginID = config.login1
		if loginID == config.loginID2:
			loginID = config.login2
		if loginID == config.loginID3:
			loginID = config.login3
		if loginID == config.loginID4:
			loginID = config.login4
		if loginID == config.loginID5:
			loginID = config.login5
		if loginID == config.loginID6:
			loginID = config.login6
			
		if "@" in loginID:
			a,b = loginID.split('@')
			email.append(a)
			Hr[row].insert(18, a)
			Hr[row][2] = a
		else:
			email.append(loginID)
			Hr[row].insert(18, loginID)
			Hr[row][2] =loginID
	return Hr
	
	
### this  function creates an error log with a time stamp
def writeErrorLog(nomatch):
	now = format(datetime.date.today())
	nows = str(now)
	noMatchName = nows +'_unMatchedReport_' + HRtail
	with open(noMatchName, 'w') as f:
			[f.write('{0},{1}\n'.format(key, value)) for key, value in nomatch.items()]
	print("Error Log file created for" ,HRtail,"! Saved as ", noMatchName)

def writeStats(dictio):
	now = format(datetime.date.today())
	nows = str(now)
	dictName = nows+"_ProgressReport.csv"
	#with open(dictName, 'w') as f:
			#[f.write('{0},{1}\n'.format(key, value)) for key, value in dictio.items()]
	with open(dictName, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(dictio)
	
	
	
### this  function creates a new updated canvas file with a time stamp
def newCanvas(nc):
	now = format(datetime.date.today())
	nows = str(now)
	newCanName = nows+"_UpdatedCanvasFile.csv"
	with open(newCanName, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(nc)
	print("##################################################################################################################")
	print("Successfully exported ",newCanName)
	print("and it is ready to be uploaded to canvas!")

	
### this function updates a column in the canvas file 
def updateCanvas(ca, hr, col, scale):
	#
	noMatchDict = {} # or dict()
	noMatchDict['name'] = 'email'
	nomatches = int(0)
	matches = 0 
	gradeSum = 0 
	noMatchz = []
	for row in range(1, len(hr)): # go thru each submission in hackerRank
		tuID = hr[row][2]
		grade = float(hr[row][11])
		grade = grade*scale
		hrName = hr[row][3]
		hrEmail = hr[row][16]
		if tuID in myTAlist: # if it is a TA submission, skip for now
			continue
			
		for rowz in range(2, len(ca)-1):  # match with their respective canvas slot
			canvasID = ca[rowz][2]
			if canvasID == tuID:
				ca[rowz][col] = grade
				gradeSum += grade
				matches+=1
				break
			if rowz == len(ca)-2:
				#print("we could not match canvas id with submission associated with", tuID)
				noMatchz.append(hr[row][16])
				noMatchDict[hrName] = hrEmail
				nomatches+=1
				
	if len(noMatchDict)>1:
		writeErrorLog(noMatchDict)		
	print('-------------------------------------------------------------------------------------------------------------')
	tt = len(hr)-1
	hrMean = gradeSum/matches
	#hrMean = gradeSum/tt
	realAvg = gradeSum/total_students
	subRate = (matches/total_students)*100
	avgDict.append([ca[0][col],realAvg, subRate, hrMean])
	return(matches,ca)
			

def getCol(hrtail):
	col = 1
	HRname = hrtail.lower()
	h = HRname.split('_')
	hh = h[0:len(h)-2]
	for i in range(0,len(Canheader)):
		thing = Canheader[i]
		thing = thing.lower()
		canName = thing.split()
		cName = canName[0:len(h)-2]
		if cName==hh:
			return i
		if i == len(Canheader)-1:
			print("no column in canvas was found associated with this assignment!")
			col = int(input("Enter the column to edit in CANVAS, refer to CanvasColumn.xlsx file in TA drive: "))
			return col+3 
	
root = tkinter.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root,title='SELECT ALL HACKERANK files')
fileList = list(filez)
	
for i in range(0, len(fileList)):
	with open(fileList[i]) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		Hr = list(csv.reader(csvDataFile))
	
	head, HRtail = os.path.split(fileList[i])
	print("You have successfully imported HR file ", HRtail)	
	numrows1 = len(Hr)          
	numcols1 = len(Hr[0])
	col = getCol(HRtail)
	if col < 46:
		points = 100
	elif col >= 46 and col < 49:
		points = 50
	else:
		points = int(input("Enter how many points this assignment is worth in Canvas: "))
	
	scaleDown = points/100
	newHR = modHR(Hr)           # edit the HackeRank file first ..... 
	sb, newCa = updateCanvas(Can,newHR,col,scaleDown)  #now update the canvas File!
	subPercent = sb/total_students
	

newCanvas(newCa)
writeStats(avgDict)
print("You have just updated ", len(fileList),"assignments!\nThank you for using grader.py!")
print("To provide feedback or report bugs, email Victor at tug86727@temple.edu")
	
	
	
	
	
	