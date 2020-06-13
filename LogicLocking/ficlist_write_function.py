
from fic import *
from bench_to_spice_format import extract_from_bench

	


################INPUTS###################################		
bench_no = ['test']
#########################################################	

for bb in range(0,len(bench_no)):
	fnetlist='c'+bench_no[bb]+'.scp'

	####extracted netarray is different for bench and spice format.t###
	fbench='./Benchmark/'+bench_no[bb]+'.bench'
	inp,keyname,outp,netarray=extract_from_bench(fbench)
	
	inp.append('HI')
	complete_list = LUT_LOCK_replacement(fnetlist,outp,inp)
	print("complete_list", complete_list)
		
	test_filename='ficlist_c'+bench_no[bb]+'.csv' 
	f_hd=open(test_filename,'w')
	for i in range(len(complete_list)):
		if i == len(complete_list)-1:
			f_hd.write(str(complete_list[i])+'\n')
		else:
			f_hd.write(str(complete_list[i])+',')
							
	f_hd.close()
	
