#This program grabs the Profiles file and takes all of its words to create a dictionary
#OF BIGRAMS!!!
file_string='../Data/Tweets/gm.guestProfileColumn'


#file_string='../Data/Tweets/toyProfiles.txt'


import json
import os
import time
start_time = time.time()
stoplist=[]
g=open('../Data/stoplist.txt','r')
for w in g:
	stoplist.append(w.replace('\n', ''))

g.close()
toRemove=[]
f=open('../Data/symbols.txt')
for s in f:
	toRemove.append(s.replace('\n',''))

f.close()	
Bi_Dictionary={}
User_Bi_Dictionary={}
g = open(file_string, 'rb')

for line in g:
	line=line.strip()
	Profile=line.split('\t')
	tweet=Profile[4]			
	tweet=tweet.replace('#', ' #')
	tweet=tweet.replace('@','')		
	#Clean it
	for i in range(0,len(toRemove)):
		tweet=tweet.replace(toRemove[i],' ')
	for j in range(0,len(stoplist)):
		tweet=tweet.lower().replace(" "+stoplist[j]+" "," ")
				
	tweet.replace('  ', ' ')	
	#This is to change things like #ohio#kcco to two hashtags
	#add it to the dictionary
	words=tweet.split()	
	#Remove all hashtags. I don't need them, I have them in the other dictionary
	#Same as @
	wordlist=[]
	for i in range(0,len(words)):
		if words[i].find('#')==-1 and words[i].find('@')==-1:
			wordlist.append(words[i].lower())	
	for i in range(0,len(wordlist)-1):
		if Profile[0] in User_Bi_Dictionary.keys():
			User_Bi_Dictionary[Profile[0]].append(wordlist[i]+" "+wordlist[i+1])
		else:
			User_Bi_Dictionary[Profile[0]]=[wordlist[i]+" "+wordlist[i+1]]
			
		if wordlist[i]+" "+wordlist[i+1] in Bi_Dictionary.keys():
			Bi_Dictionary[wordlist[i]+" "+wordlist[i+1]].append(Profile[0])
		else:
			Bi_Dictionary[wordlist[i]+" "+wordlist[i+1]]=[Profile[0]]
	


#Write to a file
f = open ("../Data/BiDict.txt", 'w')
f.write(repr(Bi_Dictionary))
f.close()

f = open("../Data/User_Bi_Dictionary.txt",'w')
f.write(repr(User_Bi_Dictionary))
f.close()


g.close()
print time.time()-start_time
os.system('say "your program has finished"')

