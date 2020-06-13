from testability_chaogate_replacement import testable_chao_netlist
from random_chaogate_replacement import random_chao_netlist
from testability_final import testability
from logicsolver_chao import mixed_logic_solver
from logicsolver_chao import logic_func
from bench_to_spice_format import extract_from_bench
from finding import finding_index
from random import *
import math

	


################INPUTS###################################		
bench_no = ['test']
rows = [5000]
#########################################################	

for bb in range(0,len(bench_no)):
	
	netlist_bench='./Benchmark/c'+bench_no[bb]+'.bench' 
	
	print("bench number", bench_no[bb])
	

	fnetlist='netlist_testable_replacement.scp'
	complete_list = testability(netlist_bench,bench_no[bb],rows[bb])
	print("complete_list", complete_list)
		
	test_filename='testability_c'+bench_no[bb]+'_rows_'+str(rows[bb])+'.csv' 
	f_hd=open(test_filename,'w')
	for i in range(len(complete_list)):
		if i == len(complete_list)-1:
			f_hd.write(str(complete_list[i])+'\n')
		else:
			f_hd.write(str(complete_list[i])+',')
							
	f_hd.close()
	
