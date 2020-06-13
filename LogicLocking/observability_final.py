import csv
import sys

def recurse(node,path,temp,netarray,outpname,inp1,inp2):
	#global netarray,outpname,inp1,inp2
	temp_copy=temp[0:]
	#find children
	index1 = [index for index in range(len(inp1)) if inp1[index] == node]
	index2 = [index for index in range(len(inp2)) if inp2[index] == node]
	index=set(index1+index2)
	child=[netarray[i][1] for i in index]
	
	for i in range(0,len(child)):
		if child[i] not in outpname:
			temp.append(child[i])
			recurse(child[i],path,temp[0:],netarray,outpname,inp1,inp2)
			temp=temp_copy[0:]
			
		else:
			temp.append(child[i])
			path.append(temp)
			temp=temp[0:-1]
			
	return path		
			

def cond_observ(node,path,netarray,outpname,outp,inp1,inp2,gate):
	#global netarray,outpname,outp,inp1,inp2,gate
	dict={'AND':1,'NAND':1,'OR':0,'NOR':0}
	name_secinp=[]
	val_secinp=[]
	for i in range(0,len(path)):
		tmp_name_secinp=[]
		tmp_val_secinp=[]
		for j in range(0,len(path[i][:])):
			ind=outp.index(path[i][j])
			tmp_gate=gate[ind]
			if (j==0):
				if((tmp_gate!='XOR') and (tmp_gate!='XNOR')):
						if(inp1[ind]!=node):
								tmp_name_secinp.append(inp1[ind])
								tmp_val_secinp.append(dict[tmp_gate])
						elif(inp2[ind]!=node):
								tmp_name_secinp.append(inp2[ind])
								tmp_val_secinp.append(dict[tmp_gate])
			else:
				if((tmp_gate!='XOR') and (tmp_gate!='XNOR')):
						if(inp1[ind]!=path[i][j-1]):
								tmp_name_secinp.append(inp1[ind])
								tmp_val_secinp.append(dict[tmp_gate])
						elif(inp2[ind]!=node):
								tmp_name_secinp.append(inp2[ind])
								tmp_val_secinp.append(dict[tmp_gate])
		name_secinp.append(tmp_name_secinp)
		val_secinp.append(tmp_val_secinp)
	return name_secinp,val_secinp
			
def different_output_paths(path, outpname):
	num_output = len(outpname)
	lists = []
	
	for i in range(0,num_output):
		gatelist_temp=[]
		for j in range(0, len(path)):
			if path[j][-1] == outpname[i]:
				gatelist_temp.append(path[j])
		if (len(gatelist_temp)!=0):
			lists.append(gatelist_temp)
	return lists
	
		
def final_count_code(nodename,nodevalue,filename):	
	c = any( isinstance(e, list) for e in nodename)
	rows = []
	fields = []
	with open(filename, 'r') as csvfile: 
		# creating a csv reader object 
		csvreader = csv.reader(csvfile) 
      
		# extracting field names through first row 
		fields = next(csvreader)
			
		# extracting each data row one by one 
		for row in csvreader: 
			rows.append(row)		
		
		if c == False:
			col = []
			index = []
			for k in range(0,len(nodename)):	
				for i in range(0,len(fields)):
					if nodename[k] == fields[i]:
						col.append(i)
			
			final_count = 0
			nodevalues = []
			for i in range(0,len(nodevalue)):
				nodevalues.append(str(nodevalue[i]))
		
			for i in range(0,len(rows)):
				val = []
				for k in range(0,len(col)):
					val.append(rows[i][col[k]])
				if val == nodevalues:
					index.append(i)
		
			final_count = len(index)
		
		else:
			col_final = []
			index = []
			for k in range(0,len(nodename)): #length of list
				col = []
				for p in range(0,len(nodename[k])): #length of sublist 
					for i in range(0,len(fields)):
						if nodename[k][p] == fields[i]:
							col.append(i)
				col_final.append(col)
				
			final_count = 0
			nodevalues = []
			for i in range(0,len(nodevalue)):
				temp = []
				for k in range(0,len(nodevalue[i])):
					temp.append(str(nodevalue[i][k]))
				nodevalues.append(temp)
		
			for i in range(0,len(rows)):	
				for k in range(0,len(col_final)):
					val = []
					for p in range(0,len(col_final[k])):
						val.append(rows[i][col_final[k][p]])
					if val == nodevalues[k]:
						index.append(i)
			index = set(index)
			final_count = len(index)/float(len(rows))
			
	return final_count
	

def observability(netarray, outpname, filename):	
	inp1=[]
	for i in range(0,len(netarray)):
		inp1.append(netarray[i][2])

	inp2=[]
	for i in range(0,len(netarray)):
		inp2.append(netarray[i][3])
	
	outp=[]
	for i in range(0,len(netarray)):
		outp.append(netarray[i][1])
	
	gate=[]
	for i in range(0,len(netarray)):
		gate.append(netarray[i][0])

	cand_outp = outp
	obs_res=[0]*len(cand_outp)

	for i in range(0,len(cand_outp)): #iterating over all gate output
		if i%10==0:
			print("observability iteration percentage:",i*100/len(cand_outp))
		tarnode=cand_outp[i]
		path = recurse(tarnode,[],[],netarray,outpname,inp1,inp2)
		lists = different_output_paths(path, outpname)
		temp_calc=[0]*(len(outpname)+1)
		if tarnode in outpname:
			temp_calc[0]=1
		for j in range(0,len(lists)):
			testlist=lists[j]
			nodename,nodevalue=cond_observ(tarnode,testlist,netarray,outpname,outp,inp1,inp2,gate)
			fcount=final_count_code(nodename,nodevalue,filename)
			temp_calc[1+j]=fcount
		sum_temp=sum(temp_calc)/float(len(outpname))
		obs_res[i]=sum_temp	
	return obs_res, cand_outp

		
