def normal_write(gatename, inp, outp, f):
	#f = open(filename, 'a')
	f.write(outp)
	f.write(' = ')
	f.write(gatename)
	f.write('(')
	for i in range (0, len(inp)-1):
		f.write(inp[i])
		f.write(', ') 
	f.write(inp[-1])
	f.write(')\n')
	#f.close()
	return 0
	
# gatename = 'OR'
# inp = ['1', '2', '3', '4']
# outp = '10'	
# filename = 'write_test.txt'
# c = normal_write(gatename, inp, outp, filename)

