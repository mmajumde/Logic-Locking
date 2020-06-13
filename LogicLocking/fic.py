from random import *
from Fan_in_cone import *
from output_impact import *
from signal_skew import *
def LUT_LOCK_replacement(fnetlist,outp,inp):
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

	out_sel=FIC_find_maximum(fnetlist,outp,inp) #selected output based on largest fan in cone
	print("selected output:\n",out_sel)
	fanin_gatelist=FIC_find_details(fnetlist,out_sel,inp) #gate list of selected output's fan in
	print("gate list in the fan in cone:\n",fanin_gatelist)
	sumfan=0
	for i in range(0,len(fanin_gatelist)):
		sumfan=sumfan+len(fanin_gatelist[i])
	print("size of gate list:\n",sumfan)
	candidate_gatelist=[] # candidate gate list for replacement based logic obfuscation
	#print(fanin_gatelist)
	for i in range(0,len(fanin_gatelist),2):
		for j in range(0,len(fanin_gatelist[i])):
			candidate_gatelist.append(fanin_gatelist[i][j])
	#print(candidate_gatelist)
	rank=[0]*len(candidate_gatelist)
	for i in range(0,len(candidate_gatelist)):
		if netarray[candidate_gatelist[i]-1][1] in outp:
			rank[i]=1
		else:
			rank[i]=find_impact_output(fnetlist,outp,netarray[candidate_gatelist[i]-1][1])
	skewval=solve_signal_prob(fnetlist,inp) #probability list of all nets in the netlist
	#print("test")
	#print(skewval)
	sig_prob=[0]*len(candidate_gatelist)
	for i in range(0,len(candidate_gatelist)):
		#print(candidate_gatelist[i]-1)
		#print("test")
		#print(netarray[candidate_gatelist[i]-1][1])
		sig_prob[i]=skewval[netarray[candidate_gatelist[i]-1][1]]
	
	#print(candidate_gatelist)
	#print(rank)
	#print(skewval)
	#print(sig_prob)
	sorted_index=sorted(range(len(rank)), key=lambda k: rank[k])
	#print(sorted_index)
	count=0
	temp_list=[]#list for gate index having same output impact values
	temp_list.append(sorted_index[0])
	sorted_groups=[]
	#sepearting groups of gate index having same output impact values
	for i in range(1,len(sorted_index)):
		if(rank[sorted_index[i]]==rank[sorted_index[i-1]]):
			temp_list.append(sorted_index[i])
		else:
			sorted_groups.append(temp_list)
			temp_list=[]
			temp_list.append(sorted_index[i])
	sorted_groups.append(temp_list)
	#print(sorted_groups)
	sort_final=[]
	
	for i in range(0,len(sorted_groups)):
		temp=[0]*len(sorted_groups[i])
		for j in range(0,len(sorted_groups[i])):
			temp[j]=sig_prob[sorted_groups[i][j]]
		#print(temp)
		sort_temp=sorted(range(len(temp)), key=lambda k: temp[k], reverse=True) #sorted index based on signal skew
		for j in sort_temp:
			sort_final.append(sorted_groups[i][j])
	#print(sort_final)
	sorted_gateindex=[]
	for i in sort_final:
		sorted_gateindex.append(candidate_gatelist[i])
	#print(sorted_gateindex)
	return sorted_gateindex
	
'''			
fnetlist='ISCAS85.scp'
inp=['I1','I2','I3','I4','I5','HI']
outp=['O1','O2']
LUT_LOCK_replacement(fnetlist,outp,inp)
'''
'''
fnetlist='add_sub4_orig.scp'
inp=['a0','b0_in','a1','b1_in','a2','b2_in','a3','b3_in','ci']
outp=['s0','s1','s2','s3','cout']
ans=LUT_LOCK_replacement(fnetlist,outp,inp)
print(ans)
'''