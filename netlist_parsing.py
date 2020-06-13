

#function for extracting from spice format
def spice_to_array(fnetlist):
	netarray=[] # 2D list for gate description
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
				if count!=0:
					if word not in netname:
						netname.append(word)
				count=count+1
			netarray.append(temp)
	return netarray

#function for extracting from bench format for the SAT solver in HOST 15 website	
def extract_from_spice(fnetlist):
	inpname=[]
	keyname=[]
	outpname=[]
	with open(fnetlist) as fnet:
		netarray=[]
		for line in fnet:
			line=line.strip()
			if (not (line.startswith('#'))) and (line):
				if line.startswith('INPUT'):
					line=line.strip('INPUT( ')
					line=line.strip(')\n')
					if line.startswith('keyinput'):
						keyname.append(line)
					else:
						inpname.append(line)
				elif line.startswith('OUTPUT'):
					line=line.strip('OUTPUT( ')
					line=line.strip(')\n')
					outpname.append(line)
				else:
					line=line.replace(' =','')
					line=line.replace('(',' ')
					line=line.replace(',','')
					line=line.replace(')','')
					#print(line)
					temp_array=line.split()
					
					# for word in line:
						# if count==0:
							# temp_array.append(word)
						# count=count+1
					netarray.append(temp_array)
		#print(inpname)
		#print(keyname)
		#print(outpname)
		#print(netarray)
				
	return inpname,keyname,outpname,netarray	

# fnetlist='../benchmarks/original/c17.bench'
# i,k,o,n=extract_from_spice(fnetlist)
# print(n)
# print(i)
# print(k)
# print(o)