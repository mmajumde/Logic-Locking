def minterms(list_a):
	for i in range(0, len(list_a)):
		list_a[i] = '{0:04b}'.format(list_a[i])
	c = ''.join(list_a)
	temp = []
	for j in range (0, len(c)):
		#print j
		if c[j] == '1':
			#print c[j]
			temp.append(j)
	return temp


#a = [0, 1, 2, 3, 5, 6]
# a=list(range(0,4))
# c = minterms(a)	
# print(c)