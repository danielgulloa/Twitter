
import json
import os
import time
import ast




file_string="../Data/User_Words.txt"
Labels=['liberal', 'conservative']



f1=open(file_string,'rb')
f2=open("../Data/UsersProbs.txt",'w')

'''
user1 %Lib %Cons    if unknown: 0.5 0.5
'''
count_lib=0
count_cons=0	
for line in f1:
	tmp_dict={}
	tmp_dict=ast.literal_eval("{"+line+"}")
	
	known=False

	criteria = (Labels[0] in tmp_dict[tmp_dict.keys()[0].lower()] or Labels[0]+'s' in tmp_dict[tmp_dict.keys()[0].lower()]) and (Labels[1] not in tmp_dict[tmp_dict.keys()[0].lower()] and Labels[1]+'s' not in tmp_dict[tmp_dict.keys()[0].lower()])		
	if(criteria):
		f2.write("".join(tmp_dict.keys())+"\t1\t0\n")
		known=True
		count_lib=count_lib+1
		
	criteria = (Labels[1] in tmp_dict[tmp_dict.keys()[0].lower()] or Labels[1]+'s' in tmp_dict[tmp_dict.keys()[0].lower()]) and (Labels[0] not in tmp_dict[tmp_dict.keys()[0].lower()] and Labels[0]+'s' not in tmp_dict[tmp_dict.keys()[0].lower()])							
	if (criteria):
		f2.write("".join(tmp_dict.keys())+"\t0\t1\n")
		known=True
		count_cons=count_cons+1
		
	criteria = (Labels[1] in tmp_dict[tmp_dict.keys()[0].lower()] or Labels[1]+'s' in tmp_dict[tmp_dict.keys()[0].lower()]) and (Labels[0] in tmp_dict[tmp_dict.keys()[0].lower()] or Labels[0]+'s' in tmp_dict[tmp_dict.keys()[0].lower()])	
	if (not known):
		f2.write("".join(tmp_dict.keys())+"\t0.5\t0.5\n")

print count_lib
print count_cons

f1.close()
f2.close()
