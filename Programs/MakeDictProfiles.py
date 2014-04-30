#This program grabs the Profiles file and takes all of its words to create a dictionary
file_string='../Data/Tweets/gm.guestProfileColumn'
#file_string='../Data/Tweets/toyProfiles.txt'


import json
import os
import time
start_time = time.time()

WordDict={}
hashtags = {}
at = {}

stoplist=[]
g=open('../Data/stoplist.txt','r')
for w in g:
	stoplist.append(w.replace('\n', ''))
	
g.close()

toRemove=[]
g=open('../Data/symbols.txt')
for s in g:
	toRemove.append(s.replace('\n',''))

g.close()	

Dictionary=[]
User_Words={}

g = open(file_string, 'rb')
for line in g:
	line=line.strip()
	Profile=line.split('\t')
	tweet=Profile[4]
		
	#Clean it
	for i in range(0,len(toRemove)):
		tweet=tweet.replace(toRemove[i],' ')
	
	
	#This is to change things like #ohio#kcco to two hashtags
	tweet=tweet.replace('#', ' #')
	tweet=tweet.replace('  ', ' ')
	
	#add it to the dictionary
	words=tweet.split()
	user_w=[]
	for i in range(0,len(words)):
		if words[i].lower() not in stoplist:
			user_w.append(words[i].lower())
	
	
	
	
	User_Words[Profile[0]]=user_w
	for i in range(0,len(words)):
		if words[i].find('#')!=-1:
			if(hashtags.has_key(words[i].lower())):
				aux=hashtags[words[i].lower()]
				aux.append(Profile[0].encode('ascii', 'ignore'))
				hashtags[words[i].lower().encode('ascii', 'ignore')]=aux
			else:
				hashtags[words[i].lower().encode('ascii', 'ignore')]=[Profile[0].encode('ascii', 'ignore')] 		
				
				
		if words[i].find('@')!=-1:
			if(at.has_key(words[i].lower())):
				aux=at[words[i].lower()]
				aux.append(Profile[0].encode('ascii', 'ignore'))
				at[words[i].lower().encode('ascii', 'ignore')]=aux
			else:
				at[words[i].lower().encode('ascii', 'ignore')]=[Profile[0].encode('ascii', 'ignore')] 
			
			
					
		if words[i].lower().encode('ascii,','ignore') in WordDict.keys():
			WordDict[words[i].lower().encode('ascii,','ignore')].append(Profile[0])
		else:
			WordDict[words[i].lower().encode('ascii,','ignore')]=[Profile[0]]
	


g.close()

f = open ("../Data/WordDict.txt", 'w')
f.write(repr(WordDict))
f.close()


g=open ("../Data/AllWords.txt",'w')
g.write(repr(Dictionary))
g.close()

g=open("../Data/Hashtags.txt",'w')
g.write(repr(hashtags))
g.close()

g=open("../Data/Ats.txt",'w')
g.write(repr(at))
g.close()

g=open("../Data/User_Words.txt",'w')
g.write(repr(User_Words))
g.close()


print time.time()-start_time
os.system('say "your program has finished"')



