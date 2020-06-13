

def signal_prob(gatename,P1,P2,flag):
	# arg=[]
	# #arg[0]: name of the gate
	# #arg[1]: probability of 1 at the first input
	# #arg[2]: probability of 1 at the second input
	
	# for val in args:
		# arg.append(val)
	# P1=arg[1]
	# P2=arg[2]
	# flag=arg[3]
	prob_high=0
	if gatename=='AND':
		if(flag==0):
			prob_high=P1*P2
		else:
			prob_high=P1
	elif gatename=='OR':
		if (flag==0):
			prob_high=(P1*P2)+(P1*(1-P2))+((1-P1)*P2)
		else:
			prob_high=P1
	elif gatename=='XOR':
		if (flag==0):
			prob_high=(P1*(1-P2))+((1-P1)*P2)
		else:
			prob_high=0
	elif gatename=='NAND':
		if (flag==0):
			prob_high=1-(P1*P2)
		else:
			prob_high=(1-P1)
	elif gatename=='NOR':
		if (flag==0):
			prob_high=1-((P1*P2)+(P1*(1-P2))+((1-P1)*P2))
		else:
			prob_high=(1-P1)
	elif gatename=='XNOR':
		if (flag==0):
			prob_high=1-((P1*(1-P2))+((1-P1)*P2))
		else:
			prob_high=1
	
	return prob_high
def solve_signal_prob(fnetlist,inpname):
	netname=[] # list of all nets in the netlist
	netarray=[] # 2D list for gate description
	with open(fnetlist) as fnet:
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

	#print(netarray)
	#print(netname)
	inpdict={}
	
	#creating dictionary for input net name and probability (of 1) value
	for i in range(0,len(inpname)):
		if(inpname[i]=='HI'):
			inpdict[inpname[i]]=1
		elif(inpname[i]=='LO'):
			inpdict[inpname[i]]=0
		else:
			inpdict[inpname[i]]=0.5
	

	netval={} #dictionary for keeping the value of each net
	skewval={} #dictionary for keeping the value of signal probability skew
	netstatus={} #dictionary for keeping the update status (valid/invalid) of each net
	for i in range(0,len(netname)):

		#initializing value of each net
		if netname[i] in inpname:
			netval[netname[i]]=inpdict[netname[i]]
		else:
			netval[netname[i]]=0
		#print(netval)
		#initializing status of each net
		if netname[i] in inpname:
			netstatus[netname[i]]=1
		else:
			netstatus[netname[i]]=0

	#print(netval)
	#print(netstatus)

	#solver
	#iterating each gate
	i=0
	while (i<len(netarray)):
		gate_name=netarray[i][0]
		o_p=netarray[i][1]
		i_p1=netarray[i][2]
		i_p2=netarray[i][3]
		
		#if the inputs of the gate are evaluated yet
		if (netstatus[i_p1]==1)&(netstatus[i_p2]==1):
			#print(True)
			#print(o_p)
			if(i_p1==i_p2):
				flag=1
			else:
				flag=0
			
			netval[o_p]=signal_prob(gate_name,netval[i_p1],netval[i_p2],flag)
			skewval[o_p]=abs(2*netval[o_p]-1)
			netstatus[o_p]=1
			i=i+1
		else:
			#print(False)
			#taking the element to the last of the list for considering later
			temp=netarray[i]
			del(netarray[i])
			netarray.append(temp)
		#print(netarray)
		#print(netval)
		#print(netstatus)
	print(skewval)
	return skewval

'''
fnetlist='lut_lock.scp'
inp=['I1','I2','I3','I4','I5','I6', 'I7']
outp=['O1','O2']

ans=solve_signal_prob(fnetlist,inp)
print(ans)
'''
