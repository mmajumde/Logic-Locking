def finding_index(char_file):
	char_chao=[]
	with open(char_file) as f_chao:
		for line in f_chao:
			count=0
			for word in line.split(','):
					if count==5: 
						char_chao.append(int(word))
					count=count+1
	#print(char_chao)

	and_val = 1
	or_val = 7
	xor_val = 6	
	nand_val = 14
	nor_val = 8	
	xnor_val = 9

	and_index = 1
	or_oindex = 1
	xor_index = 1
	nand_index = 1
	nor_oindex = 1
	xnor_index = 1

	for i in range(0, len(char_chao)):
		if char_chao[i] == and_val:
			and_index = i+1
			break
	for i in range(0, len(char_chao)):
		if char_chao[i] == or_val:
			or_index = i+1
			break
	for i in range(0, len(char_chao)):
		if char_chao[i] == xor_val:
			xor_index = i+1
			break				
	for i in range(0, len(char_chao)):
		if char_chao[i] == nand_val:
			nand_index = i+1
			break	
	for i in range(0, len(char_chao)):
		if char_chao[i] == nor_val:
			nor_index = i+1
			break
	for i in range(0, len(char_chao)):
		if char_chao[i] == xnor_val:
			xnor_index = i+1
			break		
	return and_index, or_index, xor_index, nand_index, nor_index, xnor_index

			
	

# char_file='./Characterization 65 chip new/characterization_65_chip_last_32_iteration_1.csv'
# a, b, c, d, e, f = finding_index(char_file) 
# print(a)
# print(b)			
# print(c)			
# print(d)
# print(e)			
# print(f)	