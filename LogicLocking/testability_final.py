from observability_final import observability  
from controllability_final import controllability 
from bench_to_spice_format import extract_from_bench
from bench_to_spice_format import write_in_scp
from logicsolver import mixed_logic_solver
import numpy as np
from random import *
import csv
import sys
import math

def netlist_to_netarray(fnetlist):			
	netarray=[] # 2D list for gate description
	netname=[]
	with open(fnetlist) as fnet:
		for line in fnet:
			'''
			line=line.replace(" ","")
			line=line.strip("\n")
			'''
			count=0
			temp=[]
			for word in line.split():
				#print(word)
				temp.append(word)
				if count!=0:
					if word not in netname:
						netname.append(word)
				count=count+1
			netarray.append(temp)
	return netarray	
	
def generating_truth_table(fspice, inpname, outpname, inpval, rows):
	filename = 'bool_truthtable_'+fspice+'.csv'
	netarray=netlist_to_netarray(fspice)
	f=open(filename,'w')
	netval = mixed_logic_solver(fspice,inpname,inpval,outpname)
	net_keys = netval.keys()
	#print("input name", inpname)
	#print(net_keys)
	temp_net_keys=list(net_keys)
	for j in range(len(net_keys)):
		#f.write(str(net_keys[j]))
		f.write(str(temp_net_keys[j]))
		f.write(',')
	f.write('\n')
	linp = len(inpname)
	for i in range(0,rows):
		cryptogen = SystemRandom()
		inpval = [cryptogen.randrange(2) for i in range(linp)]
		#adding HI and LO if there exists NOT gates in the schematic
		
		for i in range (0,len(inpname)):
			if inpname[-2] == 'HI' and inpname[-1] == 'LO':
				del inpval[-1]
				del inpval[-1]
				inpval.append(1)
				inpval.append(0)
				break
			else:
				for i in range (0,len(netarray)):			
					if netarray[i][3] == 'LO':
						del inpval[-1]
						inpval.append(0)
						break
				for i in range (0,len(netarray)):
					if netarray[i][3] == 'HI':
						del inpval[-1]
						inpval.append(1)
						break	
		#print("inpval", inpval)		
		netval = mixed_logic_solver(fspice,inpname,inpval,outpname)
		#print(netval)
		for j in netval:
			output = netval[j]
			#print(output)
			f.write(str(output))
			f.write(',')
		f.write('\n')
		
	f.close()
	return filename	
	
def testability(fbench,bench_no,rows):
	inpname,keyname,outpname,net = extract_from_bench(fbench)	
	fspice = write_in_scp(fbench,bench_no)
	netarray=netlist_to_netarray(fspice)
	#print(netarray)	
	linp=len(inpname)
	#print("length of input name",linp)
	cryptogen = SystemRandom()
	inpval = [cryptogen.randrange(2) for i in range(linp)]
	#adding HI and LO if there exists NOT gates in the schematic
	for i in range (0,len(netarray)):
		if netarray[i][3] == 'HI':
			inpname.append('HI')
			inpval.append(1)
			break
	for i in range (0,len(netarray)):		
		if netarray[i][3] == 'LO':
			inpname.append('LO')
			inpval.append(0)
			break 
	print("generating truth table .....")			
	filename = 	generating_truth_table(fspice, inpname, outpname, inpval, rows)	#HI and LO is already appended in inpname
	print("truth table generation complete\n")	
	print("calculating observability .....\n")	
	obs, outp = observability(netarray, outpname, filename)
	print("observability calculation complete\n")	
	print("calculating controllability .....\n")
	prob, nodes= controllability(netarray, filename)
	print("controllability calculation complete\n")
	test = []
	for i in range(0,len(obs)):
		temp = obs[i]*prob[i]
		test.append(temp)
	index = sorted(range(len(test)), key=lambda k: test[k], reverse = True)
	#print("observability",obs)
	#print(outp)
	#print("controllability", prob)
	#print(nodes)
	#print("testability", test)
	#print("sorted index", index)
	return index


# bench_no = 499
# fbench = './Benchmark Circuits/c'+str(bench_no)+'.bench'
# rows = 10 #number of test vectors to be evaluated
# testability(fbench,bench_no,rows)
