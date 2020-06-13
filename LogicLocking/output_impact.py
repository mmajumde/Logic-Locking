from random import *
def find_impact_output(fnetlist,outp,node):
#find how many output is affected by the 'node' under test
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
	#print("netarray", netarray)

	
	#finding the impact of the given node on all outputs
	
	parent=[node] # parent input node
	#print ("parent node", parent)
	child=['dummy'] #child node initialized to pass the while loop check
	impacted_output=[] # list for output nodes impacted by 'node' under test
	while(len(child)>0):
		child=[] # child list initialized to 0 
		for i in range(0,len(parent)):
			#print(i)
			for j in range(0,len(netarray)):
				#print("length of netarray", len(netarray))
				#print("j", j)
				#print(parent[i])
				#print(netarray[j][2])
				#print(netarray[j][3])
				if((parent[i]==netarray[j][2]) | (parent[i]==netarray[j][3])):
					temp=netarray[j][1] # output child node of the current parent node
					#print(temp)
					if temp not in child:
						if (temp in outp):
							if(temp not in impacted_output):
								impacted_output.append(temp)
								#print(impacted_output)
						else:
							child.append(netarray[j][1])
							#print(child)
			
						
		parent=child				
		
	
	return len(impacted_output)	
'''
fnetlist='lut_lock.scp'
inp=['I1','I2','I3','I4','I5','I6','I7']
outp=['O1','O2']
'''
'''
fnetlist='add_sub4_orig.scp'
inp=['a0','b0_in','a1','b1_in','a2','b2_in','a3','b3_in','ci']
outp=['s0','s1','s2','s3','cout']
# fnetlist='ISCAS85.scp'
# inp=['I1','I2','I3','I4','I5','HI']
# outp=['O1','O2']
node='n1_2'
ans=find_impact_output(fnetlist,outp,node)
print(ans)
'''
