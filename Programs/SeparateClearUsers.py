classes={"Conservatives","Liberals"}

keywords={"conservative","liberal"}

Group1=""
Group2=""
f1=open('../Data/WordDict.txt','r')
for line in f1:
	List = line.replace("\'","").replace(" \n","").split(": ")
	if 'conservative' in List[0].lower():
		Group1+=List[1]
	if 'liberal' in List[0].lower():
		Group2+=List[1]

Group1=Group1.replace("][",", ")
Group2=Group2.replace("][",", ")

#Remove repetitions:
Conservatives=Group1.split(", ")
Liberals=Group2.split(", ")
Conservatives[-1]=Conservatives[-1].replace("]","")
Conservatives[0]=Conservatives[0].replace("[","")
Liberals[-1]=Liberals[-1].replace("]","")
Liberals[0]=Liberals[0].replace("[","")
Liberals=list(set(Liberals))
Conservatives=list(set(Conservatives))


FinalConservatives=[]
#Remove intersections
for user in Conservatives:
	if user not in Liberals:
		FinalConservatives.append(user)

FinalLiberals=[]
for user in Liberals:
	if user not in Conservatives:
		FinalLiberals.append(user)


g=open('../Data/Conservatives','w')
g.write(str(FinalConservatives))
g.close()
g=open('../Data/Liberals','w')
g.write(str(FinalLiberals))
g.close()
	
