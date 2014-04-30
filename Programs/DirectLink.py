
allUsers=[]
f=open('../Data/Tweets/gm.userFriendMapping','r')
for line in f:
	allUsers.append(line.split("\t")[0])

f.close()

f=open('../Data/Tweets/gm.userFriendMapping','r')
g=open('../Data/DirectLink.csv','a')
for line in f:
	user_list=line.split("\t")
	tmp_list=user_list[1].split(", ")
	tmp_list[-1]=tmp_list[-1].replace("]\n","")
	tmp_list[0]=tmp_list[0].replace("[","")
	g.write(user_list[0]+"\t")
	links=list(set(allUsers) & set(tmp_list))
	g.write(str(links)+"\n")

g.close()
f.close() 


