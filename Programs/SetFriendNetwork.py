import json
import time
start_time = time.time()
file = '../Data/Tweets/gm.userFriendMapping'
#file = '../Data/Tweets/toyFriendMap'
FM=[]
Users=[]
Network={}
h=open(file, 'rb')
lines=h.readlines()
h.close()
h=open(file, 'rb')
for line in h:	
	line=line.strip()
	U = line.split('\t')
	Users.append(U[0])

h.close()
h=open(file, 'rb')
for line in h:
	line=line.strip()
	FriendMap = line.split('\t')
	FM=FriendMap[1].split(', ')
	FM[0]=FM[0].replace('[','')
	FM[-1]=FM[-1].replace(']','')
	
	mutual=[]
	follows=[]
	
	for friend in FM:
		if friend in Users:
			if FriendMap[0] in lines[Users.index(friend)]: #FriendMap[0] and friend are mutual friends
				mutual.append(friend)
			else:
				#This program might have a small bug. When somebody is following somebody, I should also updated the followed_by for the other person
				follows.append(friend)
				if friend in Network.keys():
					A = Network[friend]["followed_by"]
					A.append(FriendMap[0])
					Network[friend]={"mutual":Network[friend]["mutual"], "follows": Network[friend]["follows"], "followed_by":A}
				else:
					Network[friend]={"mutual":[], "follows": [], "followed_by":[FriendMap[0]]}	
				
				
				
		else:
			follows.append(friend)
			if friend in Network.keys():
				A = Network[friend]["followed_by"]
				A.append(FriendMap[0])
				Network[friend]={"mutual":Network[friend]["mutual"], "follows": Network[friend]["follows"], "followed_by":A}
			else:
				Network[friend]={"mutual":[], "follows": [], "followed_by":[FriendMap[0]]}	
	
	if FriendMap[0] in Network.keys():
		followed_by=Network[FriendMap[0]]["followed_by"]
	else:
		followed_by=[]	
	Network[FriendMap[0]]={"mutual":mutual, "follows": follows, "followed_by": followed_by}

print Network
#Write to a file
f = open ("../Data/Net.txt", 'w')
f.write(repr(Network))
f.close()


print (time.time()-start_time)
