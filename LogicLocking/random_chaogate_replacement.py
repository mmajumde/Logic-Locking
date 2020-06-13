from random import *
def random_chao_netlist(fnetlist,c):
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
	print(netarray)

	#modify : replacing c number of gate randomly out of total n gate
	#c=3
	n=len(netarray)
	clist=[] # gate no. to be replace
	klist=[]
	kname=[]
	temp=n
	for i in range(0,c):
		while (temp in clist)|(temp>n-1):
			temp=randint(0,n-1)
		#print(temp)
		clist.append(temp)
		kname.append(netarray[temp][0])
		#print(kname)
		netarray[temp][0]='CHAO'
		netarray[temp].append('k'+str(temp+1))
		klist.append('k'+str(temp+1))
		#print(klist)
			

	#write modified netlist to another file
	fmod=open('netlist_random_replacement.scp','w')
	for i in range(0,n):
		for j in range(0,len(netarray[i])):
			fmod.write(netarray[i][j])
			fmod.write(' ')
		if i<=n:
			fmod.write('\n')
	return klist,kname
	close(fmod)
	#print(klist)


	