


#from pyeda.inter import *
import math 

def bench_write_reconfig(f,outp,inplist,internal_nodename,minterm_index):
	#f=open(fname,'a')
	#internal_nodename:
	#minterm_index: index of 1's in the truthtable
	netarray_local=[]
	#creating inverted inputs
	linp=len(inplist) #length of primary input and key
	for i in range(0,linp):
		if (inplist[i] not in inplist[0:i]):
			f.write('inv'+internal_nodename+'_'+inplist[i]+' = '+'not'+'('+inplist[i]+')'+'\n')
	
	for i in range(0,len(minterm_index)):
		
		f.write(internal_nodename+str(i)+' = '+'and'+'(')
		bin_temp=format(minterm_index[i],'0'+str(len(inplist))+'b')
		# print("min_term:",i)
		# print(bin_temp)
		# print("lenofinp:",linp)
		# print("inplist:",inplist)
		#print(bin_temp)
		#print(minterm_index[i])
		for j in range(0,linp):
			if int(bin_temp[j])==1:
				f.write(inplist[j])
			else:
				f.write('inv'+internal_nodename+'_'+inplist[j])
			if(j<linp-1):
				f.write(', ')
		f.write(')\n')
	f.write(outp+' = '+'or'+'(')
	for i in range(0,len(minterm_index)):
		f.write(internal_nodename+str(i))
		if(i<len(minterm_index)-1):
				f.write(', ')
		
	f.write(')\n')
	#f.close()
	
	
def simplify_operation(netarray,internal_nodename):
#breaks one multiple input operation into several two input operaion
	outp=netarray[0]
	gate_name=netarray[1]
	inplist=netarray[2:len(netarray)]
	#print(inplist)
	gate_dict={'nand':'and','nor':'or','xnor':'xor'}
	flag=1
	if (gate_name in gate_dict):
		flag=0 # indicates an inverting operation
		gate_name_mod=gate_dict[gate_name] #multi input inverted operation are done using multi input non inverted and inverter at the end. 
	else:
		gate_name_mod=gate_name
	linp=len(inplist)
	#print(linp)
	# if linp%2==1:
		# linp_even=linp-1
	# else:
		# linp_even=linp
	# print(linp_even)
	net_array_return=[]
	temparray=[0]*4
	stage= int(math.ceil(math.log(linp,2)))
	#print("stage:",stage)
	
	
	lone_pair1='null'
	
	for i in range(0,stage):
		sub_stage= int(math.floor(linp/2))
	
		for j in range(0,sub_stage):
			#print("sub_stage:",sub_stage)
			#if there is any lone pair gate
			temparray=[]
			if i==0:
				temparray.append(internal_nodename+str(i)+'$'+str(j))
				temparray.append(gate_name_mod)
				temparray.append(inplist[2*j+0])
				temparray.append(inplist[2*j+1])
				net_array_return.append(temparray)
				
			elif i==stage-1:
				if flag==1:
					temparray.append(outp)
				else:
					temparray.append(outp+'$temp')	
				temparray.append(gate_name_mod)
				temparray.append(internal_nodename+str(i-1)+'$'+str(2*j+0))
				temparray.append(internal_nodename+str(i-1)+'$'+str(2*j+1))
				net_array_return.append(temparray)
			else:
				temparray.append(internal_nodename+str(i)+'$'+str(j))
				temparray.append(gate_name_mod)
				temparray.append(internal_nodename+str(i-1)+'$'+str(2*j+0))
				temparray.append(internal_nodename+str(i-1)+'$'+str(2*j+1))
				net_array_return.append(temparray)
			#print("net_array_return:",net_array_return)
			
		temparray=[]
		if (linp%2==1):
			#print("linp is odd")
			if(lone_pair1=='null'):
				lone_pair1=inplist[linp-1]
				#print("lone_pair1:",lone_pair1)
			else:
				lone_pair2=internal_nodename+str(i-1)+'$'+str(linp-1)
				#print("lone_pair2:",lone_pair2)
				if i==stage-1:
					if flag==1:
						temparray.append(outp)
					else:
						temparray.append(outp+'$temp')	
					temparray.append(gate_name_mod)
					temparray.append(lone_pair1)
					temparray.append(lone_pair2)
					lone_pair1=internal_nodename+str(i)+'$'+str(j+1)
					net_array_return.append(temparray)
				else:
					temparray.append(internal_nodename+str(i)+'$'+str(j+1))
					temparray.append(gate_name_mod)
					temparray.append(lone_pair1)
					temparray.append(lone_pair2)
					lone_pair1=internal_nodename+str(i)+'$'+str(j+1)
					net_array_return.append(temparray)
			
		#print("net_array_return:",net_array_return)	
		linp=int(linp/2)		
		sub_stage=math.floor(linp/2)		
		#print("sub_stage:",sub_stage)		 
	if flag==0:
		#print("Test")
		temparray=[]
		temparray.append(outp)
		temparray.append('not')
		temparray.append(outp+'$temp')
		net_array_return.append(temparray)	
		#print("net_array_return:",net_array_return)	
	return net_array_return
		
		
	
 	
			
		
		
	
# fname='../benchmarks/original/test_replaced_netlist.bench'
# outp='y'
# inplist=['k3','k2','x1','x0']
# minterm_index=[7,10,14,15]
# internal_nodename='i0_'
# bench_write_reconfig(fname,outp,inplist,'ii',minterm_index)


# netarray=['y','nand','a','b','c','d','e','f','g','h','i','j','k']
# netarr=simplify_operation(netarray,'zz')
# print(netarr)
