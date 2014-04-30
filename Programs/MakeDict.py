#This program grabs a file and takes all of its words to create a dictionary

import json



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
f=open('../Data/Tweets/gm.json','r')
for line in f:
	line=line.strip()
	aa=line.split('\t')
	tweet=json.loads(aa[-1])
	
	#Clean it
	for i in range(0,len(toRemove)):
		tweet["text"]=tweet["text"].replace(toRemove[i],' ')
	
	
	#add it to the dictionary
	words=tweet["text"].split()
	for i in range(0,len(words)):
		if words[i].find('#')!=-1:
			if(hashtags.has_key(words[i].lower())):
				aux=hashtags[words[i].lower().encode('ascii','ignore')]
				aux.append(Profile[0])
				hashtags[words[i].lower().encode('ascii','ignore')]=aux
			else:
				hashtags[words[i].lower().encode('ascii','ignore')]=[Profile[0]] 		
				
				
		if words[i].find('@')!=-1:
			if(at.has_key(words[i].lower())):
				aux=at[words[i].lower()]
				aux.append(tweet["user"]["id_str"].encode('ascii', 'ignore'))
				at[words[i].lower().encode('ascii', 'ignore')]=aux
			else:
				at[words[i].lower().encode('ascii', 'ignore')]=[tweet["user"]["id_str"].encode('ascii', 'ignore')] 
			
			
			
		if (not at.has_key(words[i].lower().encode('ascii', 'ignore'))) and (not hashtags.has_key(words[i].lower().encode('ascii', 'ignore'))):
			if words[i].lower().encode('ascii', 'ignore') not in stoplist and words[i].lower().encode('ascii', 'ignore') not in Dictionary:					
				Dictionary.append(words[i].lower().encode('ascii', 'ignore'))



f.close()
