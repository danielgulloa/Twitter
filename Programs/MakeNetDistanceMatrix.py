

f=open('../Data/Tweets/gm.userFriendMapping','r')
h=open('../Data/DistMatrix.csv','a')
for line in f:
	lista1=line.split("\t")[1].split(", ");
	lista1[-1]=lista1[-1].replace("]\n","")
	lista1[0]=lista1[0].replace("[","")
	g=open('../Data/Tweets/gm.userFriendMapping2','r')
	h.write(line.split("\t")[0]+"\t")
	finalList=[]
	for line2 in g:
		lista2=line2.split("\t")[1].split(", ");
        	lista2[-1]=lista2[-1].replace("]\n","")
        	lista2[0]=lista2[0].replace("[","")
		finalList.append(len(list(set(lista2)&set(lista1))))
	h.write(str(finalList)+"\n")
	
