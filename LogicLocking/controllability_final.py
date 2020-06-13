import csv
import sys
import math

def controllability(netarray, filename):
	rows = []
	fields = []
	with open(filename, 'r') as csvfile: 
		# creating a csv reader object 
		csvreader = csv.reader(csvfile) 
      
		# extracting field names through first row 
		#fields = csvreader.next()
		fields = next(csvreader)
			
		# extracting each data row one by one 
		for row in csvreader: 
			rows.append(row)	
		
		final = []
		flag = 0
		
		nodes = []
		for j in range(0,len(netarray)):
			nodes.append(netarray[j][1]);
		
		
		for j in range(0,len(netarray)):
			inp1 = netarray[j][2];
			inp2 = netarray[j][3];
			
			#count1 and count2 represent the column index
			count1 = 0
			count2 = 0
			col1 = []
			col2 = []
			for i in range (0,len(fields)):
				if inp1 == fields[i]:
					count1 = i;
				if inp2 == fields[i]:
					count2 = i;
			
			#extracting the values of columns in col1 and col2
			for i in range(0, len(rows)):
				col1.append(rows[i][count1])
				col2.append(rows[i][count2])
			
			#a,b,c,d keeps track of how many combinations of 00, 01, 10 and 11 exists 
			a = 0
			b = 0
			c = 0
			d = 0
			temp = []
			for i in range(0,len(col1)):
				if (col1[i] == '0' and col2[i] == '0'):
					a = a + 1
				elif (col1[i] == '0' and col2[i] == '1'):
					b = b + 1
				elif (col1[i] == '1' and col2[i] == '0'):
					c= c + 1
				else: 
					d = d + 1	
			temp.append(a)
			temp.append(b)
			temp.append(c)
			temp.append(d)
			final.append(temp)
		
		#logth contains the value of controllability
		prob = []
		logth = 0
		for j in range(0,len(final)):
			inp1 = netarray[j][2];
			inp2 = netarray[j][3];
			if inp1 == inp2:
				flag = 1
			else:
				flag = 0
			x = final[j]
			sum = 0
			for k in range(0,4):
				temp = x[k]/float(len(rows))
				sum = sum + temp*temp
			if flag == 0:			
				logth = math.log((1/sum),4)
			else:
				logth = math.log((1/sum),2)
			prob.append(logth)	
		index = sorted(range(len(prob)), key=lambda k: prob[k], reverse = True)
	return prob, nodes

