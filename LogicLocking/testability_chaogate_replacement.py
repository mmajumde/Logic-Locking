from random import *
def testable_chao_netlist(fnetlist,clist):
	#fnetlist='ISCAS85.scp'
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

	#modify : replacing c number of gate randomly out of total n gate
	#c=3
	n=len(netarray)
	#clist=[] # gate no. to be replace
	klist=[]
	kname=[]
	
	for i in range(0,len(clist)):
		#print(clist)
		kname.append(netarray[clist[i]][0])
		#print(kname)
		netarray[clist[i]][0]='CHAO'
		netarray[clist[i]].append('k'+str(clist[i]+1))
		klist.append('k'+str(clist[i]+1))
		#print(klist)
			

	#write modified netlist to another file
	fmod=open('netlist_testable_replacement.scp','w')
	for i in range(0,n):
		for j in range(0,len(netarray[i])):
			fmod.write(netarray[i][j])
			fmod.write(' ')
		if i<=n:
			fmod.write('\n')
	return klist,kname
	close(fmod)
	#print(klist)

# bench_no = 17
# netlist_original = './Benchmark Circuits/c'+str(bench_no)+'.scp'
# [keyname,keygate]=testable_chao_netlist(netlist_original,[3,5])	