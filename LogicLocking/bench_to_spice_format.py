from boolean_model_mod import *

#function for extracting from bench format	
def extract_from_bench(fnetlist):
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
		# print(inpname)
		# print(keyname)
		# print(outpname)
		# print(netarray)
				
	return inpname,keyname,outpname,netarray	
	
	
#function for converting to scp format
def write_in_scp(fnetlist, bench_no):
	inpname, keyname, outpname, netarray = extract_from_bench(fnetlist)
	#making multiple input gates to two input gates
	larray=len(netarray)
	#print(larray)

	narr_mod=[]
	#simplified netlist: using only 2 input gates
	for i in range(0,larray):
		larrel=len(netarray[i]) #length of narr element
		o_p=netarray[i][0] #output
		gname=netarray[i][1] #gate name
		i_p=netarray[i][2:larrel] #input list
	
		if len(i_p)>2: #checking if the current gate has more than 2 inputs
			simparr_temp=simplify_operation(netarray[i],'zi'+str(i)+'$')
			len_simparr_temp=len(simparr_temp)
			#put simplified netlist for the complex gate in the main netlist
			for j in range(0,len_simparr_temp):
				narr_mod.append(simparr_temp[j])
		else:
			narr_mod.append(netarray[i])
	#print(narr_mod)
	lnarr_mod=len(narr_mod)

	#print(lnarr_mod)
	
	filename = 'c'+str(bench_no)+'.scp'
	spice = open(filename, 'w')
	for i in range (0, len(narr_mod)):
		if narr_mod[i][1] == 'not':
			spice.write('XOR ')
			spice.write(narr_mod[i][0] + ' ')
			spice.write(narr_mod[i][2] + ' ')
			spice.write('HI' + '\n')
		elif narr_mod[i][1] == 'buf':
			spice.write('XOR ')
			spice.write(narr_mod[i][0] + ' ')
			spice.write(narr_mod[i][2] + ' ')
			spice.write('LO' + '\n')	
		else:
			str1 = narr_mod[i][1]
			spice.write(str1.upper() + ' ')
			spice.write(narr_mod[i][0] + ' ')
			spice.write(narr_mod[i][2] + ' ')
			spice.write(narr_mod[i][3] + '\n')
	spice.close()		
	return filename

	
# fnetlist = './Benchmark Circuits/ISCAS85.bench' 
# extract_from_bench(fnetlist)	