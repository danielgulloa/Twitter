import json
import os
import time
import ast
start_time = time.time()

f_bi="../Data/BiDict.txt"
f_up="../Data/UpdatedProbs.txt"




AllUsers=[]
FirstProb=[]
SecondProb=[]
f_probs=open(f_up,'r')
for user in f_probs:
	user_probs=user.split("\t")
	AllUsers.append(user_probs[0])
	FirstProb.append(user_probs[1])
	SecondProb.append(user_probs[2])

f_probs.close()


TEXT=""

f_dict=open(f_bi,'r')
g=open("../Data/BiProbsFromUsers.txt",'w')
h=open("../Data/BigramsWhoseUsersWeDontHaveProfile.txt",'w')
for w in f_dict:	
		bi_dict={}
		bigram=w.split(":")[0].replace("'","").replace("{","").replace("}","")
		users_of_this_word=w.split(":")[1].replace("[","").replace("]","").replace(" ","").replace("'","").replace("\n","").split(",")
		users_of_this_word=list(set(users_of_this_word))#remove repetitions
		if(len(users_of_this_word)>1):		
			word_first_prob=0
			word_second_prob=0
			found=0					
			for guy in users_of_this_word:
				if guy in AllUsers:
					ind = AllUsers.index(guy)
					word_first_prob+=float(FirstProb[ind])
					word_second_prob+=float(SecondProb[ind])
					found+=1
					
			if(found>0):				
				g.write(bigram+"\t"+str(1.0*word_first_prob/found)+"\t"+str(1.0*word_second_prob/found)+"\t"+str(found)+"\n")
				#print bigram+"\t"+str(1.0*word_first_prob/found)+"\t"+str(1.0*word_second_prob/found)
			else:
				h.write(bigram)


g.close()
h.close()
f_dict.close()








'''
---------------------
Send an email:
---------------------
'''


import smtplib
gmail_user = "danielatemory@gmail.com"
gmail_pwd = "new passwor"
FROM = 'danielatemory@gmail.com'
TO =['dgarci8@emory.edu']
SUBJECT = "Your program has finished running in the server in "+str(time.time()-start_time)+"seconds"  
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
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






