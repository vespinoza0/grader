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
JScolumn = 0
pyColumn = 0
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

for i in range(0,len(Canheader)):

	thing = Canheader[i]
	thing = thing.lower()
	canName = thing.split()
	#cName = canName[0:len(h)-2]
	if "variables" in canName and "javascript" in canName:
		JScolumn = i
	if "variables" in canName and "python" in canName:
		pyColumn = i

###############################################################


### this function gets the unique TU emai and inserts in the second column of the HR list
def modHR(Hr):
	email = []
	present = datetime.datetime.now()
	deadline = datetime.datetime(2018,2,21)
	
	for row in range(1, len(Hr)):
		loginID =Hr[row][2]
		d = Hr[row][1].split('/')
		year = int(d[0])
		month = int(d[1])
		day = int(d[2])
		subdate = datetime.datetime(year,month,day)
		# update scoring system changed on 2/21/18
		#if subdate > deadline: 
			#lolwut
		if subdate <= deadline:
			grade = float(Hr[row][11])
			if grade == 10:
				Hr[row][11] = 30
			elif grade == 40:
				Hr[row][11] = 70
				
		
		
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

	
def checkpoint(Can,jscol,pycol):
	checkList = []
	b = ['student','JS1','JS2','JS3', 'Py1', 'Py2']
	checkList.append(b)
	for i in range(2,len(Can)-1):
		student = Can[i][2]
		checks = 0
		for j in range(jscol,jscol+10):
			score = Can[i][j]
			if score:  
				score1 = float(score)
				if score1 >=70:
					checks +=1
			if not score: # if there is no element
				score = 0
				Can[i][j] = score
		#print("this student has this many checks: ", checks)
		templist = [student, '0', '0', '0', '0', '0']
		if checks >=3 and checks <6:
			templist[1] = '1' 
		elif checks >=6 and checks <10:
			templist[1] = '1'
			templist[2] = '1'
		
		elif checks == 10:
			templist[1] = '1'
			templist[2] = '1'
			templist[3] = '1'
	
		checksp = 0
		for k in range(pycol,pycol+10):
			score = Can[i][k]
			if score:
				score1 = float(score)
				if score1 >=70:
					checksp +=1
				if not score:
					score = 0
					Can[i][k] = score
				
	
		if checksp >= 5 and checksp < 10:
			templist[4] = '1'
		
		elif checksp == 10:
			templist[4] = '1'
			templist[5] = '1'

		checkList.append(templist)
	now = format(datetime.date.today())
	nows = str(now) 
	with open(nows+"_projectEligibility.csv", "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(checkList)
	
	
	
### this function updates a column in the canvas file 
def updateCanvas(ca, hr, col, scale):
	noMatchDict = {} # empty dict()
	noMatchDict['name'] = 'email'
	nomatches = int(0)
	matches = 0 
	gradeSum = 0 
	oldgradeSum = 0
	hrGradeSum = 0 
	noMatchz = []
	for row in range(1, len(hr)): # go thru each submission in hackerRank
		tuID = hr[row][2]
		grade = float(hr[row][11])
		if grade == 0:
			continue
		grade = grade*scale
		hrName = hr[row][3]
		hrEmail = hr[row][16]
		if tuID in myTAlist: # if it is a TA submission, skip for now
			continue
		for rowz in range(2, len(ca)-1):  # search canvas match with their respective canvas slot
			canvasID = ca[rowz][2]
			if canvasID == tuID:
				matches+=1
				hrGradeSum += grade
				oldgrade = float(ca[rowz][col])
				oldgradeSum += oldgrade
				if oldgrade < grade:
					#print("old grade is ", oldgrade)
					#print("new grade is ", grade)
					ca[rowz][col] = grade
					
				break
			if rowz == len(ca)-2:
				#print("we could not match canvas id with submission associated with", tuID)
				noMatchz.append(hr[row][16])
				noMatchDict[hrName] = hrEmail
				nomatches+=1
				
	for i in range(2,len(ca)-1):
		grade = float(ca[i][col])
		gradeSum += grade
				
	if len(noMatchDict)>1:
		writeErrorLog(noMatchDict)		
	print('---------------------------------------------------------------------------------------------------------------')
	tt = len(hr)-1
	hrMean = hrGradeSum/matches
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
		# if "variables" in cName and "javascript" in cName:
			# print("variables in javascript in column :", i)
			# JScolumn = i
		# if "data" in cName and "python" in cName:
			# pyColumn = i
			# print("data types in python in column :", i)
		if cName==hh:
			# print("header #", i)
			# print(cName)
			# print("found it!")
			return i
		if i == len(Canheader)-1:
			print("no column in canvas was found associated with this assignment!")
			col = int(input("Enter the column to edit in CANVAS, refer to CanvasColumn.xlsx file in TA drive: "))
			return col+3 
	
root = tkinter.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root,title='SELECT ALL HACKERANK FILES')
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
checkpoint(newCa,JScolumn,pyColumn)
writeStats(avgDict)
print("You have just updated ", len(fileList),"assignments!\nThank you for using grader.py!")
print("To provide feedback or report bugs, email Victor at tug86727@temple.edu")
	
	
	
	
	
	