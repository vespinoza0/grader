import csv
import tkinter
from tkinter import filedialog
import os
import datetime
import config

getMore = True
myTAlist = config.TAlist
globalMatches =0
#### Get a single Canvas CSV file to update! #############
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
	
	
### this  function creates ann error log with a time stamp
def writeErrorLog(nomatch):
	now = format(datetime.date.today())
	nows = str(now)
	noMatchName = nows +'_unMatchedReport_' + HRtail
	with open(noMatchName, 'w') as f:
			[f.write('{0},{1}\n'.format(key, value)) for key, value in nomatch.items()]
	print("Error Log file created for " ,HRtail,"! Saved as ", noMatchName)

### this  function creates a new updated canvas file with a time stamp
def newCanvas(nc):
	now = format(datetime.date.today())
	nows = str(now)
	newCanName = nows+"_UpdatedCanvasFile.csv"
	with open(newCanName, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(nc)
	print("#######################################################################")
	print("Successfully exported ",newCanName)
	print("and it is ready to be uploaded to canvas!")

	
### this function updates a column in the canvas file 
def updateCanvas(ca, hr, col, scale):
	#
	noMatchDict = {} # or dict()
	noMatchDict['name'] = 'email'
	nomatches = int(0)
	matches = 0 
	noMatchz = []
	for row in range(1, len(hr)): # go thru each submission in hackerRank
		tuID = hr[row][2]
		grade = float(hr[row][11])
		hrName = hr[row][3]
		hrEmail = hr[row][16]
		if tuID in myTAlist: # if it is a TA submission, skip for now
			continue
			
		for rowz in range(2, len(ca)-1):  # match with their respective canvas slot
			canvasID = ca[rowz][2]
			if canvasID == tuID:
				ca[rowz][col] = grade*scale
				matches+=1
				break
			if rowz == len(ca)-2:
				#print("we could not match canvas id with submission associated with", tuID)
				noMatchz.append(hr[row][16])
				noMatchDict[hrName] = hrEmail
				nomatches+=1
				
	if len(noMatchDict)>1:
		writeErrorLog(noMatchDict)				

	return (matches,ca)
			

def getCol(hrtail):
	col = 1
	if "Variables_in_JavaScript_" in hrtail:
		col = 17
	elif "Data_Types_in_JavaScript_" in hrtail:
		col = 18
	elif "Console_Input_and_Output_in_JavaScript_" in hrtail:
		col = 19
	elif "Operators_in_JavaScript_" in hrtail:
		col = 20
	elif "Conditional_Code_in_JavaScript_" in hrtail:
		col = 21
	elif "Flow_Control_in_JavaScript_" in hrtail:
		col = 22
	elif "Loops_in_JavaScript_" in hrtail:
		col = 23
	elif "Debugging_in_JavaScript" in hrtail:
		col = 24	
	elif "Functions_in_JavaScript_" in hrtail:
		col = 25
	elif "Objects_in_JavaScript_" in hrtail:
		col = 26
	elif "Code_Sprint_1_" in hrtail:
		col = 1 
	elif "Code_Sprint_2_" in hrtail:
		col = 2 	
	elif "Code_Sprint_3_" in hrtail:
		col = 3 
	elif "Code_Sprint_4_" in hrtail:
		col = 4 
	elif "Code_Sprint_5_" in hrtail:
		col = 5 	
	elif "Code_Sprint_6_" in hrtail:
		col = 6 
	else:
		print("no column in canvas was found associated with this assignment!")
		col = int(input("Enter the column to edit in CANVAS, refer to CanvasColumn.xlsx file in TA drive: "))
		
	return col+3
		
	
	

while(getMore):
	#### lets get a HR file and put it in a list
	print("Please Select HackerRank CSV file")  ####### 
	HRfile = filedialog.askopenfilename(title = "Select HackerRank file",filetypes = (("CSV files","*.csv"),("all files","*.*")))  # get directory +filename.csv
	head, HRtail = os.path.split(HRfile)
	with open(HRfile) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		Hr = list(csv.reader(csvDataFile))
	print("You have successfully imported HR file ", HRtail)	
	numrows1 = len(Hr)          # 3 rows in your example
	numcols1 = len(Hr[0])

	#col = col+3  ####### i think, double check the google doc 
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
	subPercent = subPercent*100
	print( "%.2f" % subPercent," percent of students have submitted ", HRtail)
	print(len(newHR)-1," students out of ", total_students," have completed this assignment")
	decide = int(input("Do you wish to continue updating? yes=1, no=0 "))

	if decide == 1:
		getMore = True
	if decide == 0:
		getMore = False
		newCanvas(newCa)
		print("Thank you for using grader.py! \nTo provide feedback or report bugs, email Victor at tug86727@temple.edu")

