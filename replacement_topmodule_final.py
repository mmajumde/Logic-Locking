from netlist_parsing import *
from boolean_model_mod import *
from finding_minterms import *
import math
import random
from normal_write import *
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b","--bench",help="input the name of benchmark circuit")
parser.add_argument("-r", "--replace_perc", type=float,
                    help="input replacement percentage")

parser.add_argument("-k", "--keylen", type=int,
                    help="input keylength for each reconfigurable gate")

parser.add_argument("-m", "--method", type=int,
                    help="input 0 for testability, 1 for random, 2 for 100% based replacement")
args = parser.parse_args()
		
#fname='../benchmarks/original/c432_enc_12.5perc_key5_purscstest.bench'
fname='/home/sabuj/LogicLocking/Benchmark/'+args.bench+'_enc_'+str(args.replace_perc)+'perc_key'+str(args.keylen)+'_riscv.bench'

#extracting information from the original netlist
#fnetlist='../benchmarks/original/'+args.bench+'.bench'
fnetlist='/home/sabuj/LogicLocking/Benchmark/'+args.bench+'.bench'
#fnetlist='../benchmarks/original/c432.bench'
print(fnetlist)
inp,key,outp,narr=extract_from_spice(fnetlist)
#print(narr)

larray=len(narr)
print(larray)

narr_mod=[]
#simplified netlist: using only 2 input gates
for i in range(0,larray):
	larrel=len(narr[i]) #length of narr element
	o_p=narr[i][0] #output
	gname=narr[i][1] #gate name
	i_p=narr[i][2:larrel] #input list
	
	if len(i_p)>2: #checking if the current gate has more than 2 inputs
		simparr_temp=simplify_operation(narr[i],'zi'+str(i)+'$')
		len_simparr_temp=len(simparr_temp)
		#put simplified netlist for the complex gate in the main netlist
		for j in range(0,len_simparr_temp):
			narr_mod.append(simparr_temp[j])
	else:
		narr_mod.append(narr[i])
#print(narr_mod)
lnarr_mod=len(narr_mod)

print(lnarr_mod)
#random insertion index
replace_perc=args.replace_perc/100.0
#replace_perc=0.125
print(replace_perc)
num_replace=int(replace_perc*lnarr_mod)
#num_replace=3
print("replaced gate count:",num_replace)
if args.method==0:
	ri=np.genfromtxt('testability_c432_rows_1000.csv', delimiter=',')
	#ri=np.genfromtxt('testability_ctest_rows_5000.csv', delimiter=',')
	ri=ri[0:num_replace]
elif args.method==1:
	ri=random.sample(list(range(0,lnarr_mod)),num_replace)
else:
	ri=list(range(0,lnarr_mod))
#ri=[16,38,43,67,121,130,141,150,216,223]
#ri=random.sample(list(range(0,lnarr_mod)),num_replace)
#ri=sorted(ri)
#ri=[77,137,159,233,374]
#num_replace=len(ri)
#print("replacement list:",ri)
#print replace gates
'''
for i in range(0,num_replace):
	print(narr_mod[int(ri[i])][1])
'''
ri_count=0
#key=['keyinput0','keyinput1','keyinput2','keyinput3','keyinput4','keyinput5','keyinput6','keyinput7']
#key=['keyinput0','keyinput1','keyinput2','keyinput3']
#LUT model
keylen=args.keylen
#keylen=5
key=[]
for i in range(0,keylen*num_replace):
	key.append('keyinput'+str(i))
	
ftable=np.genfromtxt('characterization_last_32_iteration_nominal_med.csv', delimiter=',')
#ftable=np.genfromtxt('characterization_set2_subset_1.csv', delimiter=',')
#funct_table=[int(ftable[i,5]) for i in range(2**keylen)]
if keylen==5:
	func_start=32
else:
	func_start=0

func_end=func_start+2**keylen
funct_table=[int(ftable[i,5]) for i in range(func_start,func_end)]

#funct_table=[element%16 for element in range(2**keylen)]
print(funct_table)
#func_table=list(range(0,16))+list(range(0,16))
#func_table=[1,7,6,14,8,9,1,15,15,15,15,15,15,15,15,15]
#func_table=[1,7,6,14,8,9,1]+[15]*(2**keylen-7)
#func_table=[15,15,15,15,15,15,0,15,15,15,15,0,0,0,0,0]
mterms=minterms(funct_table)
print(mterms)
print("len of mterms:",len(mterms))
#print(mterms)



f=open(fname,'w')


#write input list to the file
for i in range(0,len(inp)):
	f.write('INPUT('+inp[i]+')\n')

#f.write('\n')

#write key list to the file
for i in range(0,len(key)):
	f.write('INPUT('+key[i]+')\n')

#f.write('\n')

#write output list to the file
for i in range(0,len(outp)):
	f.write('OUTPUT('+outp[i]+')\n')

#f.close()
gatecount=0

for i in range(0,lnarr_mod):
	lnarrel=len(narr_mod[i]) #length of narr element
	o_p=narr_mod[i][0] #output
	gname=narr_mod[i][1] #gate name
	i_p=narr_mod[i][2:lnarrel] #input list
	
	if gname=="not":
		if len(i_p)!=1:
			print("problem found at ",i)
	
	if i in ri:
		gatecount=gatecount+1
		print("gatename:",gname)
		if (gname=='not'):
			#print(i_p)
			#print(i_p[0])
			i_p.append(i_p[0])
			#print(i_p)
		i_p_key=key[keylen*ri_count:keylen*(ri_count+1)]+i_p
		ri_count=ri_count+1
		iname='p'+str(i)+'$'
		bench_write_reconfig(f,o_p,i_p_key,iname,mterms)
	else:
		normal_write(gname,i_p,o_p,f)

f.close()

		

	
	

