from random_chaogate_replacement import random_chao_netlist
from testability_chaogate_replacement import *
from testability_final import testability
from logicsolver_chao import mixed_logic_solver
from logicsolver_chao import logic_func
from bench_to_spice_format import extract_from_bench
from finding import finding_index
from random import *
import math
import csv
import sys 
import time
import numpy as np


###result directory
result_dir="/home/sabuj/results/logiclocking/" #provide your own result directory

####specific input. e.g choose a particular opcode for all analysis
mode=1 # mode =0 selectes normal mode; mode=1 selects customized input mode
ctrl_val=[0,0,1,0,0] #selective op code-> AND:00000, OR:10000, XOR:01000, ADD: 11000, SUB: 11010, SHL: 00100, SRL: 10100, SRA: 10101 

start = time.time()

#netlist is in .scp format	
def create_netarray(netlist):	
	netname = []
	netarray = []
#making netarray from scp
	with open(netlist_original) as fnet:
			for line in fnet:
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

cryptogen = SystemRandom()

################INPUTS###################################		
#bench_no = [17, 432, 880, 1355, 1908,3540]
bench_no = ["test"]
#replace_percentage = [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00]
#replace_percentage = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00]
replace_percentage = [0.25]
#replace_percentage = [0.1]
#replace_percentage = [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60]
#no_of_inputs = [15, 100, 200, 200]  #different number of inputs where for each input key varies to generate challenge
#no_of_inputs = [15, 100, 300, 400]  #different number of inputs where for each input key varies to generate challenge
no_of_inputs = [15]  #different number of inputs where for each input key varies to generate challenge
observation=50; # no. of measurement to find the hamming distance between responses from correct and random key
#rows = [1000, 1000, 1000, 1000]
rows = [5000]
#########################################################	
kb=10 #keybits
####################finding 10 random chips#################
############################################################
for bb in range(0,len(bench_no)):
	
	netlist_bench='./Benchmark/c'+bench_no[bb]+'.bench' 
	inpname,keyname,outpname,net = extract_from_bench(netlist_bench)   #extracting inpname, keyname and outpname from bench
	print(inpname)
	
	linp=len(inpname)
	loutp = len(outpname)
	print('length of output ' + str(loutp))
	inpsize = 2**linp
	print("length of input",linp)

	netlist_original = 'c'+bench_no[bb]+'.scp'
	netarray = create_netarray(netlist_original)
	#print("netarray", netarray)
	#############generating different inputs to apply to the circuit##############################
	inpval = []
	temp = []
	for i in range (0,len(netarray)):
		if netarray[i][3] == 'HI':
			inpname.append('HI')
			break
	for i in range (0,len(netarray)):		
		if netarray[i][3] == 'LO':
			inpname.append('LO')
			break 	

	temp = [cryptogen.randrange(2) for i in range(linp)]
	for p in range(0,no_of_inputs[bb]):
		while (temp in inpval):
			temp = [cryptogen.randrange(2) for i in range(linp)]
			if mode==1:
				temp[-6:-3]+temp[-2:len(temp)]=ctrl_val
		
		#adding HI and LO if there exists NOT gates in the schematic
		if inpname[-2] == 'HI' and inpname[-1] == 'LO':
			temp.append(1)
			temp.append(0)
		else:	
			if inpname[-1] == 'HI':
				temp.append(1)
			if inpname[-1] == 'LO':
				temp.append(1)
		inpval.append(temp)		
#####################################################################################################
	print("bench number", bench_no[bb])
	#print("input value",inpval)
	#print("length of input value", len(inpval))
	#print("input name", inpname)
	#print("output name", outpname)
	#print("input size", inpsize)
	
#############testability list#############	
	fnetlist='netlist_testable_replacement.scp'
	complete_testable_list = []
	filename = 'testability_c'+str(bench_no[bb])+'_rows_'+str(rows[bb])+'.csv'
	with open(filename, 'r') as csvfile: 
		# creating a csv reader object 
		csvreader = csv.reader(csvfile) 
			
		# extracting each data row one by one 
		for row in csvreader: 
			complete_testable_list.append(row)
				
		#print("testability list",complete_testable_list[0])	
		
		len_complete = len(complete_testable_list[0])
		print("length of complete list", len_complete)
    		
#############testable replacement##########	
	for aa in range(0,len(replace_percentage)):
		len_clist = int(math.ceil(replace_percentage[aa]*len_complete))
		#print("length of replaced list", len_clist)
		clist = []
		for i in  range(0,len_clist):
			clist.append(int(complete_testable_list[0][i]))
		#print("replaced gates", clist)

		[keyname,keygate]=testable_chao_netlist(netlist_original,clist)
		#print("keyname",keyname)
		#print("keygate", keygate)
		keyval=[0]*len(keyname)
		lkey=len(keyname)
		#num_keyval=np.zeros(lkey)
		
		
		hd_filename=result_dir+'nom_med_HD_test_c'+str(bench_no[bb])+'_inputs_'+str(no_of_inputs[bb])+'_rows_'+str(rows[bb])+'_perc_'+str(replace_percentage[aa])+'.csv' #chip_number in different columns
		f_hd=open(hd_filename,'w')
		
		char_file='characterization_last_32_iteration_nominal_med.csv'
		a, b, c, d, e, f = finding_index(char_file) #and, or, xor, nand, nor, xnor
		keydict={'AND':a,'OR':b,'XOR':c,'NAND':d,'NOR':e, 'XNOR':f}
		###uncomment this for netlist with key gate
		keyval_correct=[0]*len(keygate)
		for i in range(0,len(keygate)):
			keyval_correct[i]=keydict[keygate[i]]
		#print("correct keyval",keyval_correct)
		keyval=[0]*len(keyval_correct)
		###

		
		cum_HD=0.0
		cum_HD_ent = 0.0
		cum_HD_inp_ent = []
		for i in range(0,no_of_inputs[bb]):
			cum_HD_inp=0.0
			# cum_HD_ent = 0.0
			#print(i)
			resp_correct=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval_correct,outpname)
			res_cor=np.array(resp_correct)
            #print("correct_response", resp_correct)
			for j in range(0,observation):
				#print(j)
				num_keyval=np.random.randint(2**kb,size=lkey)
				keyval=list(num_keyval)
				#for jj in range(0,lkey):
					#keyval[jj]=randint(0,(2**kb)-1)
				#print("random keyval",keyval)
				resp=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval,outpname)
				#print("wrong_response", resp)
				#temp_sum=0.0
				#temp_sum_ent = 0.0
				res_now=np.array(resp)
				temp_sum=np.sum(np.abs(res_now-res_cor))
				temp_sum_ent=temp_sum
				#for k in range(0,loutp):
					#temp_sum=temp_sum+abs(resp[k]-resp_correct[k])
					#temp_sum_ent=temp_sum_ent+abs(resp[k]-resp_correct[k])
				temp_sum=temp_sum/loutp
				temp_sum_ent=temp_sum_ent/loutp
				#print(temp_sum)
				cum_HD=cum_HD+temp_sum
				cum_HD_inp=cum_HD_inp+temp_sum
				#print(cum_HD)
				if temp_sum_ent > 0.5:
					temp_sum_ent = 1-temp_sum_ent
				cum_HD_ent=cum_HD_ent+temp_sum_ent	
			cum_HD_inp=(cum_HD_inp*100)/(observation)
			#print("cum_HD_input",cum_HD_inp)
			if cum_HD_inp > 50:
				cum_HD_inp = 100-cum_HD_inp
			cum_HD_inp_ent.append(cum_HD_inp) 
		#print("cum_HD_inp_ent",cum_HD_inp_ent)	
		cum_HD=(cum_HD*100)/(observation*no_of_inputs[bb])
		cum_HD_ent=(cum_HD_ent*100)/(observation*no_of_inputs[bb])
		sum = 0.0
		for i in range(0,len(cum_HD_inp_ent)):		
			sum = sum + cum_HD_inp_ent[i]
		avg = sum/len(cum_HD_inp_ent)	
			
		print(replace_percentage[aa],'_HD_test',cum_HD)
		print(cum_HD_ent)
		print(avg)	
		f_hd.write(str(cum_HD)+'\n')
		f_hd.write(str(cum_HD_ent)+'\n')
		f_hd.write(str(avg)+'\n')
							
	f_hd.close()
   
##########Random Replacement Start###########	
		
	fnetlist='netlist_random_replacement.scp'
	
	for aa in range(0,len(replace_percentage)):
		replace = int(math.ceil(replace_percentage[aa]*len(netarray)))
		[keyname,keygate]=random_chao_netlist(netlist_original,replace)
		#print("keyname",keyname)
		#print("keygate", keygate)
		keyval=[0]*len(keyname)
		lkey=len(keyname)
		
		
		
		hd_filename='nom_med_HD_rand_c'+str(bench_no[bb])+'_inputs_'+str(no_of_inputs[bb])+'_rows_'+str(rows[bb])+'_perc_'+str(replace_percentage[aa])+'.csv'
		f_hd=open(hd_filename,'w')
		
		#char_file='./Characterization_nominal_median/characterization_last_32_iteration_nominal_med.csv'
		#a, b, c, d, e, f = finding_index(char_file) #and, or, xor, nand, nor, xnor
		keydict={'AND':a,'OR':b,'XOR':c,'NAND':d,'NOR':e, 'XNOR':f}
		###uncomment this for netlist with key gate
		keyval_correct=[0]*len(keygate)
		for i in range(0,len(keygate)):
			keyval_correct[i]=keydict[keygate[i]]
		#print("correct keyval",keyval_correct)
		keyval=[0]*len(keyval_correct)
		###

		
		cum_HD=0.0
		cum_HD_ent = 0.0
		cum_HD_inp_ent = []
		for i in range(0,no_of_inputs[bb]):
			cum_HD_inp=0.0
			# cum_HD_ent = 0.0
			#print(i)
			resp_correct=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval_correct,outpname)
			#print("correct_response", resp_correct)
			for j in range(0,observation):
				#print(j)
				num_keyval=np.random.randint(2**kb,size=lkey)
				keyval=list(num_keyval)
				#for jj in range(0,lkey):
					#keyval[jj]=randint(0,(2**kb)-1)
				#print("random keyval",keyval)
				resp=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval,outpname)
				#print("wrong_response", resp)
				#temp_sum=0.0
				#temp_sum_ent = 0.0
				res_now=np.array(resp)
				temp_sum=np.sum(np.abs(res_now-res_cor))
				temp_sum_ent=temp_sum
				#for k in range(0,loutp):
					#temp_sum=temp_sum+abs(resp[k]-resp_correct[k])
					#temp_sum_ent=temp_sum_ent+abs(resp[k]-resp_correct[k])
				#print(temp_sum)
				temp_sum=temp_sum/loutp
				temp_sum_ent=temp_sum_ent/loutp
				cum_HD=cum_HD+temp_sum
				cum_HD_inp=cum_HD_inp+temp_sum
				#print(cum_HD)
				if temp_sum_ent > 0.5:
					temp_sum_ent = 1-temp_sum_ent
				cum_HD_ent=cum_HD_ent+temp_sum_ent	
			cum_HD_inp=(cum_HD_inp*100)/(observation)
			#print("cum_HD_input",cum_HD_inp)
			if cum_HD_inp > 50:
				cum_HD_inp = 100-cum_HD_inp
			cum_HD_inp_ent.append(cum_HD_inp) 
		#print("cum_HD_inp_ent",cum_HD_inp_ent)	
		cum_HD=(cum_HD*100)/(observation*no_of_inputs[bb])
		cum_HD_ent=(cum_HD_ent*100)/(observation*no_of_inputs[bb])
		sum = 0.0
		for i in range(0,len(cum_HD_inp_ent)):		
			sum = sum + cum_HD_inp_ent[i]
		avg = sum/len(cum_HD_inp_ent)	
			
		print(replace_percentage[aa],'_HD_random',cum_HD)
		print(cum_HD_ent)
		print(avg)	
		f_hd.write(str(cum_HD)+'\n')
		f_hd.write(str(cum_HD_ent)+'\n')
		f_hd.write(str(avg)+'\n')
							
	f_hd.close()
	
end = time.time()
print('\n')
minutes, seconds= divmod(end-start, 60)
#other_time=(minutes*60+seconds)-(test_minutes*60+test_seconds)
#other_minutes, other_seconds= divmod(other_time, 60)
print('total time: ', minutes,' minutes',seconds,' seconds')
#print('testability time:', test_minutes, 'minutes',test_seconds, ' seconds')
#print('Other time:', other_minutes, 'minutes',other_seconds, ' seconds')
print('Rows: ',rows[0])
print('Inputs: ',no_of_inputs)
print('Percentage: ',replace_percentage) 
print('Observation: ',observation)

