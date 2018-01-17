import numpy as np
import csv
#import pandas as pd #print ("imported pandas!!")
import tkinter as tk
from tkinter import filedialog
import os
import datetime

getMore = True

now = format(datetime.date.today())
nows = str(now)
now2 = format(datetime.datetime.now())


print("please Select HacckerRank CSV file")
HRfile = filedialog.askopenfilename(title = "Select HackerRank file",filetypes = (("CSV files","*.csv"),("all files","*.*")))  # get directory +filename.csv
print(HRfile)
head, HRtail = os.path.split(HRfile)
 
with open(HRfile) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	Hr = list(csv.reader(csvDataFile))

numrows1 = len(Hr)    # 3 rows in your example
numcols1 = len(Hr[0])
print("rows by cols of Hr = ", numrows1,numcols1)

print("please Select Canvas CSV file")
Ca = filedialog.askopenfilename(title = "Select canvas file",filetypes = (("CSV files","*.csv"),("all files","*.*")))  # get directory +filename.csv
	
print(Ca)
 
with open(Ca) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	Can = list( csv.reader(csvDataFile) )
		
col = int(input("Enter the column to edit in Canvas: "))
col = col-1

points = int(input("Enter the how many points this assignment is worth in Canvas: "))
scaleDown = points/100;
numrows = len(Can)    # 3 rows in your example
total_students = numrows -3
numcols = len(Can[0])
print("rows by cols of Canvas = ", numrows,numcols)
print("you plan on editing canvas column ", col)

email = []

for rows in Hr:
	thing = rows[2]

for row in range(1, len(Hr)):
	thing =Hr[row][2]
	thing = thing.lower()
	Hr[row].insert(17, thing)
	
	if "@" in thing:
		a,b = thing.split('@')
		email.append(a)
		Hr[row].insert(18, a)
		Hr[row][2] = a

	else:
		email.append(thing)
		print('Was not able to find @ symbol',thing)
		Hr[row].insert(18, thing)
		Hr[row][2] =thing
		
#newHR  = np.array(Hr)
#newEmail = np.array(email)
#newHR[1:,2] = newEmail
matches = 0 
nomatches = 0

############# Time to Match TUid's!! 
noMatchz = []
for row in range(1, len(Hr)): # go thru each submission
	tuID = Hr[row][2]
	grade = float(Hr[row][11])
	
	for rowz in range(2, len(Can)-1):  # match with their respective canvas slot
		canvasID = Can[rowz][2]
		if canvasID == tuID:
			Can[rowz][col] = grade*scaleDown
			matches+=1
			break
		if rowz == numrows-2:
			print("we could not match canvas id with submission associated with", tuID)
			nomatches+=1
			noMatchz.append(Hr[row][17])
################
	
#for rowz in range(2, len(Can)-1):
#	poo = Can[rowz][2]
#	print(poo)

print("Successfully matched submissions = ",matches)  #print how many submissions were matched
print("Unmatched submissions", nomatches)		#print how many submissions were NOT matched


##WRITE NEW CANVAS FILE  #one way to write canvas file
#myfile = open('testCanvas.csv','w')
#wr = csv.writer(myfile, lineterminator='\n')
#wr.writerows(Can)
#myfile.close()

# WRITE NEW CANVAS FILE  #another way to write canvas file
newCanName = now+"_newCanvasFile.csv"
with open(newCanName, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(Can)
	
	
with open('HR_mod.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(Hr)
	
		
#Assuming noMatchz is a flat list write 
noMatchName = nows +'_unMatchedReport_' + HRtail
with open(noMatchName, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in noMatchz:
        writer.writerow([val])  