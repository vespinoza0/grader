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
	header = Hr[0]
	loginIDindex = header.index('Login ID')
	totalScoreColumn = header.index('Total score')
	percentColumn = header.index('Percentage score')
	maxColumn = header.index('Max score')
	
	for row in range(1, len(Hr)):
		loginID =Hr[row][loginIDindex]
		d = Hr[row][3].split('/')
		year = int(d[0])
		month = int(d[1])
		day = int(d[2])
		
		
		subdate = datetime.datetime(year,month,day)

		if subdate <= deadline:				# update scoring system changed on 2/21/18
			grade = float(Hr[row][totalScoreColumn])
			if grade == 10:
				Hr[row][percentColumn] = 30
				#maxScore =float(Hr[row][maxColumn])
				#Hr[row][percentColumn] = Hr[row][totalScoreColumn] / maxScore
			elif grade == 40:
				Hr[row][percentColumn] = 70
				#maxScore =float(Hr[row][maxColumn])
				#Hr[row][percentColumn] = Hr[row][totalScoreColumn]/ maxScore
			elif grade > 100:
				Hr[row][percentColumn] = 100
				
		
		
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
			Hr[row][loginIDindex] = a
		else:
			email.append(loginID)
			Hr[row].insert(18, loginID)
			Hr[row][loginIDindex] =loginID
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
	header = Can[0]
	CScol = header.index('Core Skills HackerRank (68007)')
	ILP1col = header.index('Individual Learning Path Assignment 1: IDE and GUI (121770)')
	ILP2col = header.index('Individual Learning Path Assignment 2: Core Skills (68009)')
	# print(CScol)
	# print(ILP1col)
	# print(ILP2col)
	checkList = []
	#b = ['student','JS1','JS2','JS3', 'Py1', 'Py2']  
	b = ['student','email','JS1','JS2','JS3', 'Py1', 'Py2', 'CS','ILP1','ILP2','Eligibility']
	checkList.append(b)
	for i in range(2,len(Can)-1):
		student = Can[i][0]
		email = Can[i][2]+ "@temple.edu"
		checks = 0
		#print(email)
		for j in range(jscol,jscol+10):  #loop thru JS 10 columns
			score = Can[i][j]
			if score:  
				score1 = float(score)
				if score1 >=70:
					checks +=1
			if not score:         #if there is no element
				score = 0
				Can[i][j] = score
		
		#templist = [student, '0', '0', '0', '0', '0']  # 
		templist = [student,email,'0', '0', '0', '0', '0','0','0','0','0']
		if checks >=3 and checks <6:
			templist[2] = '1' 
		elif checks >=6 and checks <10:
			templist[2] = '1'
			templist[3] = '1'
		
		elif checks == 10:
			templist[2] = '1'
			templist[3] = '1'
			templist[4] = '1'
	
		checksp = 0
		for k in range(pycol,pycol+10):  #loop thru python 10 columns
			score = Can[i][k]
			if score:
				score1 = float(score)
				if score1 >=70:
					checksp +=1
				if not score:
					score = 0
					Can[i][k] = score
	
		if checksp >= 5 and checksp < 10:
			templist[5] = '1'
		elif checksp == 10:
			templist[5] = '1'
			templist[6] = '1'
		
		#print("CoreSkills score",Can[i][CScol])
		if float(Can[i][CScol])>=70:
			templist[7] = '1'
		#print("ILP1 score",Can[i][ILP1col])
		if float(Can[i][ILP1col])>=70:
			templist[8] = '1'
		#print("ILP2 score",Can[i][ILP2col])
		if float(Can[i][ILP2col])>=70:
			templist[9] = '1'
		ss = templist[2:]
		ssSum= 0
		for k in range(len(ss)):
			aaa = int(ss[k])
			ssSum = ssSum+aaa
		if ssSum ==8:
			templist[10] = '1'
		
		
		#print(templist)
		#print(ss, "sum is",ssSum)
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
	header = hr[0]
	loginIDindex = header.index('Login ID')
	ScoreColumn = header.index('Percentage score')
	print("Percentage score index", ScoreColumn)
	for row in range(1, len(hr)): # go thru each submission in hackerRank
		tuID = hr[row][loginIDindex]
		grade = float(hr[row][ScoreColumn])  # imported HR grade
		if grade == 0:
			continue
		if grade >100:
			grade = 100
		grade = grade*scale
		hrName = hr[row][2]
		hrEmail = hr[row][17]

		if tuID in myTAlist: # if it is a TA submission, skip for now
			continue
		for rowz in range(2, len(ca)-1):  # search canvas match with their respective canvas slot
			canvasID = ca[rowz][2]
			if canvasID == tuID:			# if we match tug##### 
				matches+=1					# increment match counter
				hrGradeSum += grade
				oldgrade = float(ca[rowz][col]) # current canvas grade
				
				if oldgrade < grade:			# if oldgrade is less than grade from HR
					ca[rowz][col] = grade  		# update canvas list to higher grade
					oldgradeSum += grade        # add new higher grade
				else:
					oldgradeSum += oldgrade		# else add old original grade
				break
			if rowz == len(ca)-2:
				#print("we could not match canvas id with submission associated with", tuID)
				noMatchz.append(hr[row][16+1])
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
	print("this is the respective column : ", col)
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

