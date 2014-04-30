import json
import os
import time
import ast
start_time=time.time()



file_string="../Data/WordDict.txt"
file_string2="../Data/UserProbs_iterated.txt"
file_stop="../Data/stoplist.txt"

f_probs=open(file_string2,'rb')

stoplist=[]
f_stop=open(file_stop,'r')
for w in f_stop:
	stoplist.append(w.replace('\n', ''))

f_stop.close()






AllUsers=[]
LiberalProb=[]
ConsProb=[]
for user in f_probs:
	user_probs=user.split("\t")
	AllUsers.append(user_probs[0])
	LiberalProb.append(user_probs[1])
	ConsProb.append(user_probs[2])
f_probs.close()


TEXT=""
Error=""
people_updated=0
g=open("../Data/WordProbs.txt",'w')
f_dict=open(file_string,'rb')
for w in f_dict:	
		word_dict={}
		word_dict=ast.literal_eval("{"+w+"}")
		word=word_dict.keys()[0]
		users_of_this_word=word_dict[word]
		users_of_this_word=list(set(users_of_this_word))	
		people_updated+=1
		#print str(people_updated)+"\t"+word
		if len(users_of_this_word)>1: #get rid of words used by only one person		
			word_lib_prob=0
			word_cons_prob=0
			found=0					
			for guy in users_of_this_word:
				if guy in AllUsers:
					ind = AllUsers.index(guy)
					word_lib_prob+=float(LiberalProb[ind])
					word_cons_prob+=float(ConsProb[ind])
					found+=1
			n=found
			if(found>0):
				g.write(word+"\t"+str(1.0*word_lib_prob/n)+"\t"+str(1.0*word_cons_prob/n)+"\t"+str(n)+"\n")
			else:
				Error+=w+"\n"
				print Error
			


g.close()
f_dict.close()


import smtplib
gmail_user = "danielatemory@gmail.com"
gmail_pwd = "new passwor"
FROM = 'danielatemory@gmail.com'
TO =['dgarci8@emory.edu']
SUBJECT = "MakeWordsProb_iters.py finished in "+str(time.time()-start_time)+" seconds. File WordProbs.txt was updated"
TEXT += "No Errors"
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
...             """ % (FROM, ", ".join(TO), SUBJECT, Error)
try:
#server = smtplib.SMTP(SERVER) 
	server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	server.sendmail(FROM, TO, message)
	server.close()
	print 'successfully sent the mail'
except:
	print "failed to send mail"



