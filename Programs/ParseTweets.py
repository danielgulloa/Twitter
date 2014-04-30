import json
import os
import time

#Make as many keywords as wanted:
start_time = time.time()
keyword_set1=['liberal', 'Liberal']#, 'teamobama'] #will use str.lower()
keyword_set2=['conservative', 'Conservative']#, 'mittromney']
keywords=[keyword_set1, keyword_set2]


#Make according labels:
Labels=['liberal', 'conservative']



f=open('../Data/Tweets/gm.json','rb') 	
for line in f:
	line=line.strip()
	aa=line.split('\t')
	tweet=json.loads(aa[-1])
	
	
#Let's look for the keywords and separate these guys into different files:
g = open('../Data/Tweets/gm.guestProfileColumn', 'rb')
k=0;
users_array=[]
for addLabel in range(0,len(Labels)):
	users_array.append([])

for line in g:
	line=line.strip()
	Profile=line.split('\t')
	
	for j in range(0,len(Labels)):
		file_out = open('../Data/Tweets/'+Labels[j]+'.txt','a')
		
		for i in range(0,len(keywords)):
			if(Profile[4].lower().find(keywords[j][i])!=-1):
			#if (Profile[4].lower().find(keywords[j])!=-1):
				#Found keyword! let's put it this guy in appropriate file			
				#file_out.write(Profile[0]+"\t"+Profile[1]+"\t"+Profile[2]+"\t"+Profile[3]+"\t"+Profile[4]+"\t"+Profile[5]+"\t"+Profile[6]+"\t"+Profile[7]+"\n")	
				users_array[j].append(Profile[0])
				
		file_out.close()
	

#Maybe some cleaning would be good..... We could manually check those guys that are repeated?
#883 users are repeated in both files!!



h=open('../Data/Tweets/gm.userFriendMapping', 'rb')
f=open('../Data/Tweets/gm.json','rb') 	
j=0
TweeterUser=[''];
TweetLabelDict=[[0]*6 for i in range(1)]
for line in f:
	line=line.strip()
	aa=line.split('\t')
	tweet=json.loads(aa[-1])
	TweetLabelDict[j][5]=aa[6] #"sarcasm"
	TweetLabelDict[j][4]=aa[5] #"irony"
	TweetLabelDict[j][3]=aa[4] #"support"
	TweetLabelDict[j][2]=aa[3] #"polarity"
	TweetLabelDict[j][1]=aa[2] #"intensity"
	TweetLabelDict[j][0]=tweet["user"]["id"] #user
	TweeterUser[j]=tweet["user"]["id"] #user
	TweeterUser.append([''])
	TweetLabelDict.append([0,0,0,0,0,0])
	j=j+1



	
	
	
	

	
#file_out = open('../Data/Tweets/FriendMapLabels.txt','a')
label_counter=[[0]*10 for i in range(1)]
thresholdLib = 1.3
thresholdCons = 0.8
countLiberals=0
countConservs=0
countUndef=0
k=0

for line in h:
	line=line.strip()
	FriendMap = line.split('\t')
	FM=FriendMap[1].split(', ')
	#file_out.write(FriendMap[0]+"\t")
	label_counter.append([0,0,0,'','',-1,-1,-1,-1,-1])
	for user in FM:
		for label in range(0,len(Labels)):
			if user in users_array[label]:
				label_counter[k][label]=label_counter[k][label]+1
	label_counter[k][2]=(1.0*label_counter[k][0]+1)/(label_counter[k][1]+1)
	if label_counter[k][2]>thresholdLib:
		label_counter[k][3]=Labels[0]
		contLiberals=countLiberals+1
		
	elif label_counter[k][2]< thresholdCons:
		label_counter[k][3]=Labels[1]
		countConservs=countConservs+1
	else:
		label_counter[k][3]='Undef'
		countUndef=countUndef+1
	
	#let's look for this user in the TweetLabel and give it intensity, polarity, support, etc				
	label_counter[k][4]=FriendMap[0]
	for	i in range(0,len(TweetLabelDict)):
		if (int(label_counter[k][4])==TweetLabelDict[i][0]):
			label_counter[k][5]=TweetLabelDict[i][1]
			label_counter[k][6]=TweetLabelDict[i][2]
			label_counter[k][7]=TweetLabelDict[i][3]
			label_counter[k][8]=TweetLabelDict[i][4]
			label_counter[k][9]=TweetLabelDict[i][5]
		
	k=k+1	
	



#Everything is in label_counter!!!  We just need now to count stuff
	#look if it is liberal, and see support, polarity, intensity
	#otherwise, if it is conservative, look for the same stuff
	#I would say put everything in a matrix
Matrix=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
lib=0; cons=1; undef=2
intensity_undef = 0; intensity_non = 1; intensity_intense=2;
polarity_undef=3; polarity_pleased = 4; polarity_neutral=5; polarity_angry=6;
support_undef=7; support_sup=8; support_neutral = 9; support_oppose=10;

for i in range(0,len(label_counter)):
	if label_counter[i][3]==Labels[0]:
		intensity = label_counter[i][5]
		if intensity=="-1":
			Matrix[lib][intensity_undef]+=1
		elif intensity == "0":
			Matrix[lib][intensity_non]+=1
		else:
			Matrix[lib][intensity_intense]+=1			
		polarity=label_counter[i][6]
		if polarity=="-1":
			Matrix[lib][polarity_undef]+=1
		elif polarity == "0":
			Matrix[lib][polarity_pleased]+=1
		elif polarity == "1":
			Matrix[lib][polarity_neutral]+=1
		else:
			Matrix[lib][polarity_angry]+=1		
		support=label_counter[i][7]
		if support == "-1":
			Matrix[lib][support_undef]+=1
		elif support == "0":
			Matrix[lib][support_sup]+=1
		elif support == "1":
			Matrix[lib][support_neutral]+=1
		else:
			Matrix[lib][support_oppose]+=1
	elif label_counter[i][3]==Labels[1]:
		intensity = label_counter[i][5]
		if intensity=="-1":
			Matrix[cons][intensity_undef]+=1
		elif intensity == "0":
			Matrix[cons][intensity_non]+=1
		else:
			Matrix[cons][intensity_intense]+=1
			
		polarity=label_counter[i][6]
		if polarity=="-1":
			Matrix[cons][polarity_undef]+=1
		elif polarity == "0":
			Matrix[cons][polarity_pleased]+=1
		elif polarity == "1":
			Matrix[cons][polarity_neutral]+=1
		else:
			Matrix[cons][polarity_angry]+=1
			
		
		support=label_counter[i][7]
		if support == "-1":
			Matrix[cons][support_undef]+=1
		elif support == "0":
			Matrix[cons][support_sup]+=1
		elif support == "1":
			Matrix[cons][support_neutral]+=1
		else:
			Matrix[cons][support_oppose]+=1
	
	else:
		intensity = label_counter[i][5]
		if intensity=="-1":
			Matrix[undef][intensity_undef]+=1
		elif intensity == "0":
			Matrix[undef][intensity_non]+=1
		else:
			Matrix[undef][intensity_intense]+=1
			
		polarity=label_counter[i][6]
		if polarity=="-1":
			Matrix[undef][polarity_undef]+=1
		elif polarity == "0":
			Matrix[undef][polarity_pleased]+=1
		elif polarity == "1":
			Matrix[undef][polarity_neutral]+=1
		else:
			Matrix[undef][polarity_angry]+=1
			
		
		support=label_counter[i][7]
		if support == "-1":
			Matrix[undef][support_undef]+=1
		elif support == "0":
			Matrix[undef][support_sup]+=1
		elif support == "1":
			Matrix[undef][support_neutral]+=1
		else:
			Matrix[undef][support_oppose]+=1

			

print Matrix

	
	
f.close()
g.close()
h.close()				
print time.time()-start_time
os.system('say "your program has finished"')




	



	
