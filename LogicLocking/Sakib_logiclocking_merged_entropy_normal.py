from testability_chaogate_replacement import testable_chao_netlist
from random_chaogate_replacement import random_chao_netlist
from testability_final import testability
from logicsolver_chao import mixed_logic_solver
from logicsolver_chao import logic_func
from bench_to_spice_format import extract_from_bench
from finding import finding_index
from random import *
import math
import time

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
bench_no = ['test']
no_chip=65
#replace_percentage = [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00]
#replace_percentage = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00]
#replace_percentage = [0.05, 0.15, 0.25]
replace_percentage = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
#replace_percentage = [0.25]
no_of_inputs = [50]  #different number of inputs where for each input key varies to generate challenge
no_of_char_files = 1
observation=50; # no. of measurement to find the hamming distance between responses from correct and random key
rows = [1000]
#########################################################	
kb=10 #keybits
####################finding 10 random chips##############
char_file_no = []

cc = [cryptogen.randrange(1,66)]
for p in range(0,no_of_char_files):
	while (cc in char_file_no):
			cc = [cryptogen.randrange(1,66)]
		#print("cc",cc)	
	char_file_no.append(cc)
print("characterization file",char_file_no)	
############################################################
for bb in range(0,len(bench_no)):
	
	#netlist_bench='./Benchmark Circuits/c'+str(bench_no[bb])+'.bench' 
	netlist_bench='./Benchmark/c'+bench_no[bb]+'.bench' 
	inpname,keyname,outpname,net = extract_from_bench(netlist_bench)   #extracting inpname, keyname and outpname from bench
	linp=len(inpname)
	loutp = len(outpname)
	print('length of output ' + str(loutp))
	inpsize = 2**linp
	print("length of input",linp)

	netlist_original = './Benchmark/c'+str(bench_no[bb])+'.scp'
	netarray = create_netarray(netlist_original)
	print("netarray", netarray)
	'''
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
	print("input value",inpval)
	print("length of input value", len(inpval))
	print("input name", inpname)
	print("output name", outpname)
	print("input size", inpsize)
##########Testability start######## 
	
	start_test = time.time()
	complete_list = testability(netlist_bench,bench_no[bb],rows[bb])
	end_test=time.time()
	test_minutes, test_seconds= divmod(end_test-start_test, 60)	
	print("complete_list", complete_list)
	len_complete = len(complete_list)
	print("length of complete list", len_complete)
##########Testability end######## 

##########Testability Replacement Start###########	
	print('Test')
	fnetlist='netlist_testable_replacement.scp'
	for aa in range(0,len(replace_percentage)):
		len_clist = int(math.ceil(replace_percentage[aa]*len_complete))
		#print("length of replaced list", len_clist)
		clist = []
		for i in  range(0,len_clist):
			clist.append(complete_list[i])
		#print("replaced gates", clist)

		[keyname,keygate]=testable_chao_netlist(netlist_original,clist)
		#print("keyname",keyname)
		#print("keygate", keygate)
		keyval=[0]*len(keyname)
		lkey=len(keyname)
		
		
		hd_filename='ent_hamming_distance_testability_c'+str(bench_no[bb])+'_perc'+' '+str(replace_percentage[aa])+'.csv' #chip_number in different columns
		f_hd=open(hd_filename,'w')
		for p in range(0, len(char_file_no)):
			#char_file='./Characterization 65 chip new/characterization_65_chip_last_32_iteration_'+str(char_file_no[p][0])+'.csv'
			char_file='./Characterization_nominal_median/characterization_last_32_iteration_nominal_med.csv'
			a, b, c, d, e, f = finding_index(char_file) #and, or, xor, nand, nor, xnor
			keydict={'AND':a,'OR':b,'XOR':c,'NAND':d,'NOR':e, 'XNOR':f}
			#print("chip number", char_file_no[p][0])
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
					for jj in range(0,lkey):
						keyval[jj]=randint(0,(2**kb)-1)
					#print("random keyval",keyval)
					resp=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval,outpname)
					#print("wrong_response", resp)
					temp_sum=0.0
					temp_sum_ent = 0.0
					for k in range(0,loutp):
						temp_sum=temp_sum+abs(resp[k]-resp_correct[k])
						temp_sum_ent=temp_sum_ent+abs(resp[k]-resp_correct[k])
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
			#print(cum_HD)
			#print(cum_HD_ent)
			#print(avg)	
			
			f_hd.write(str(cum_HD)+'\n')
			f_hd.write(str(cum_HD_ent)+'\n')
			f_hd.write(str(avg)+'\n')
								
		f_hd.close()
	##########Random Replacement Start###########	
	print('Random')
	fnetlist='netlist_random_replacement.scp'
	
	for aa in range(0,len(replace_percentage)):
		replace = int(math.ceil(replace_percentage[aa]*len(netarray)))
		[keyname,keygate]=random_chao_netlist(netlist_original,replace)
		#print("keyname",keyname)
		#print("keygate", keygate)
		keyval=[0]*len(keyname)
		lkey=len(keyname)
		
		
		
		hd_filename='ent_hamming_distance_random_c'+str(bench_no[bb])+'_perc'+' '+str(replace_percentage[aa])+'.csv' #chip_number in different columns
		f_hd=open(hd_filename,'w')
		for p in range(0, len(char_file_no)):
			#char_file='./Characterization 65 chip new/characterization_65_chip_last_32_iteration_'+str(char_file_no[p][0])+'.csv'
			char_file='./Characterization_nominal_median/characterization_last_32_iteration_nominal_med.csv'
			a, b, c, d, e, f = finding_index(char_file) #and, or, xor, nand, nor, xnor
			keydict={'AND':a,'OR':b,'XOR':c,'NAND':d,'NOR':e, 'XNOR':f}
			#print("chip number", char_file_no[p][0])
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
					for jj in range(0,lkey):
						keyval[jj]=randint(0,(2**kb)-1)
					#print("random keyval",keyval)
					resp=mixed_logic_solver(char_file,fnetlist,inpname,inpval[i],keyname,keyval,outpname)
					#print("wrong_response", resp)
					temp_sum=0.0
					temp_sum_ent = 0.0
					for k in range(0,loutp):
						temp_sum=temp_sum+abs(resp[k]-resp_correct[k])
						temp_sum_ent=temp_sum_ent+abs(resp[k]-resp_correct[k])
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
			
			print(replace_percentage[aa],'_HD_random',cum_HD)	
			#print(cum_HD)
			#print(cum_HD_ent)
			#print(avg)	
			f_hd.write(str(cum_HD)+'\n')
			f_hd.write(str(cum_HD_ent)+'\n')
			f_hd.write(str(avg)+'\n')
								
		f_hd.close()
'''	
end = time.time()
print('\n')
minutes, seconds= divmod(end-start, 60)
print('total time: ', minutes,' minutes',seconds,' seconds')
print('testability time:', test_minutes, 'minutes',test_seconds, ' seconds')
print('Rows: ',rows[0])
print('Inputs: ',no_of_inputs)
print('Percentage: ',replace_percentage) 
print('Observation: ',observation)
