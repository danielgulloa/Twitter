
allUsers=[]

f1=open('../Data/DirectLink.csv','r')
for line in f1:
	allUsers.append(line.split("\t")[0])
f1.close()

f1=open('../Data/TwoLinkSeparation.csv','r')
f2=open('../Data/DirectLink.csv','r')
DL=f2.readlines()
f2.close()
g=open('../Data/ConnectivityMatrixUpdate.csv','a')
counter=0
for line in f1:
	user1 = line.split("\t")[0]
	List = line.split("\t")[1].split(", ")
	List[-1]=List[-1].replace("]\n","")
	List[0]=List[0].replace("[","")
	List2=DL[counter].replace("\'","").split("\t")[1].split(", ")
	List2[-1]=List2[-1].replace("]\n","")
	List2[0]=List2[0].replace("[","")
	Connections=int(List[counter])
	
	for number in range(0,len(List)):
			List[number]=float(List[number])/Connections
	for user2 in List2:
		if user2 in allUsers:
			List[allUsers.index(user2)]=1
		else:
			print user2
	counter+=1
	g.write(user1+"\t"+str(List)+"\n")


g.close()
f1.close()


