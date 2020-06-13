from random import *
def FIC_find_maximum(fnetlist,outp,inp):
	#fnetlist='ISCAS85.scp'
	#fnetlist='adder.scp'
	netarray=[]
	#read original netlist file
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
					# if count!=0:
						# if word not in netname:
							# netname.append(word)
					count=count+1
				netarray.append(temp)
	#print(netarray)

	
	#finding fan in cone size for all outputs
	cone_size={}
	for i in range(0,len(outp)):
		sum_FIC=0
		#node_list=[]
		FIC=[] #list of gates in the fan in cone of an output
		temp_node_new=[]
		temp_node_new.append(outp[i]) # initial node list
		#print (temp_node_new) 		
		#node_list.append(temp_node)
		count1=0
		flag1=0 #flag for determining end of fan in cone
		while(flag1==0):
			temp_node_old=temp_node_new
			#print(temp_node_old)
			FIC_temp=[]
			temp_node_new=[] # node list for stage(count1)
			#print("count1")
			#print(count1)
			for j in range(0,len(temp_node_old)):
				count2=0 # line count for netlist parsing
				flag2=0 # flag for a match with the node
				while(flag2==0):
					#print("count2")
					print(count2)
					print(netarray[count2][1])
					print(temp_node_old[j])
					
					if(netarray[count2][1]==temp_node_old[j]):
						flag2=1
						FIC_temp.append(count2+1) # save the name of gate that generates the output of candidate list
						#print(FIC_temp)
						temp_child=netarray[count2][2:4] # child node list
						#print(temp_child)
						for k in range(0,2):
							if ((temp_child[k] not in temp_node_new) & (temp_child[k] not in inp)):
								temp_node_new.append(temp_child[k])
							
					count2=count2+1
			count1=count+1
			#print(temp_node_new)
			if temp_node_new==[]:
				flag1=1
			FIC.append(FIC_temp)
			#print(FIC)
			sum_FIC=sum_FIC+len(FIC_temp)
		cone_size[outp[i]]=sum_FIC
		#print("cone size", cone_size)
	return max(cone_size)

	
def FIC_find_details(fnetlist,maxout,inp):
	#fnetlist='ISCAS85.scp'
	#fnetlist='adder.scp'
	netarray=[]
	#read original netlist file
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
					# if count!=0:
						# if word not in netname:
							# netname.append(word)
					count=count+1
				netarray.append(temp)
	#print(netarray)
	outp=[maxout]
	
	#finding fan in cone size for all outputs
	
	for i in range(0,len(outp)):
		sum_FIC=0
		#node_list=[]
		FIC=[] #list of gates in the fan in cone of an output
		temp_node_new=[]
		temp_node_new.append(outp[i]) # initial node list 
		#node_list.append(temp_node)
		count1=0
		flag1=0 #flag for determining end of fan in cone
		while(flag1==0):
			temp_node_old=temp_node_new
			#print(temp_node_old)
			FIC_temp=[]
			temp_node_new=[] # node list for stage(count1)
			#print("count1")
			#print(count1)
			for j in range(0,len(temp_node_old)):
				count2=0 # line count for netlist parsing
				flag2=0 # flag for a match with the node
				while(flag2==0):
					#print("count2")
					#print(count2)
					#print(netarray[count2][1])
					#print(temp_node_old[j])
					if(netarray[count2][1]==temp_node_old[j]):
						flag2=1
						FIC_temp.append(count2+1) # save the name of gate that generates the output of candidate list
						#print(FIC_temp)
						temp_child=netarray[count2][2:4] # child node list
						#print(temp_child)
						for k in range(0,2):
							if ((temp_child[k] not in temp_node_new) & (temp_child[k] not in inp)):
								temp_node_new.append(temp_child[k])
							
					count2=count2+1
			count1=count+1 
			#print(temp_node_new)
			if temp_node_new==[]:
				flag1=1
			FIC.append(FIC_temp)
			#print(FIC)
			
		
	return FIC
# fnetlist='ISCAS85.scp'
# inp=['I1','I2','I3','I4','I5','HI']
# outp=['O1','O2']
'''
fnetlist='lut_lock.scp'
inp=['I1','I2','I3','I4','I5','I6','I7']
outp=['O1','O2']
'''
'''
fnetlist='add_sub4_orig.scp'
inp=['a0','b0_in','a1','b1_in','a2','b2_in','a3','b3_in','ci']
outp=['s0','s1','s2','s3','cout']

ans1=FIC_find_maximum(fnetlist,outp,inp)
print(ans1)
ans2=FIC_find_details(fnetlist,ans1,inp)
print(ans2)
'''
