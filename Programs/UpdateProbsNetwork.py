import json
import os
import time
import ast
start_time = time.time()

file_string="../Data/Toys/toy_Net.txt"
file_string2="../Data/Toys/toy_UsersProbs.txt"
file_string_Write="../Data/Toys/toy_UpdatedProbs.txt"


file_string="../Data/Net.txt"
file_string2="../Data/UsersProbs.txt"
file_string_Write="../Data/UpdatedProbs.txt"
file_log="../Data/log.txt";
TEXT=""



updated=0
f1=open(file_string,'rb')
f2=open(file_string2,'rb')
g=open(file_string_Write,'w')
log=open(file_log,'w')
AllUsers=[]
LiberalProb=[]
ConsProb=[]
for user in f2:
	user_probs=user.split("\t")
	AllUsers.append(user_probs[0])
	LiberalProb.append(user_probs[1])
	ConsProb.append(user_probs[2])
f2.close()


for line in f1:
	user_net={}
	user_net=ast.literal_eval("{"+line+"}")
				
	following = user_net[user_net.keys()[0]]["follows"]
	following.extend(user_net[user_net.keys()[0]]["mutual"])
	user_LibProb=0
	user_ConsProb=0
	found=0
	ind=0
	for dude in following:
		if dude in AllUsers:
			ind=AllUsers.index(dude)	
			user_LibProb+=float(LiberalProb[ind])
			user_ConsProb+=float(ConsProb[ind])			
		else:
			log.write("Strangely, person "+dude+" was not considered before. Let's add her in UsersProbs.txt \n")
			print "Strangely, person "+dude+" was not considered before. Let's add her in UsersProbs.txt \n"
			AllUsers.append(dude)
			LiberalProb.append(0.5)
			ConsProb.append(0.5)
			user_LibProb+=0.5
			user_ConsProb+=0.5
			f2=open(file_string2,'a')
			f2.write(str(dude)+"\t"+str(0.5)+"\t"+str(0.5)+"\n")
			f2.close()
					
	if(len(following)>0):
		log.write("This is normal: "+user_net.keys()[0]+"\t"+str(1.0*user_LibProb/len(following))+"\t"+str(1.0*user_ConsProb/len(following))+"\n")				
		print "This is normal: "+user_net.keys()[0]+"\t"+str(1.0*user_LibProb/len(following))+"\t"+str(1.0*user_ConsProb/len(following))+"\n"
		g.write(user_net.keys()[0]+"\t"+str(1.0*user_LibProb/len(following))+"\t"+str(1.0*user_ConsProb/len(following))+"\n")	
		updated+=1		
	elif user_net.keys()[0] in AllUsers:
		ind=AllUsers.index(user_net.keys()[0])
	#	print "This guy had no followers:"+AllUsers[ind]+"\t"+str(LiberalProb[ind])+"\t"+str(ConsProb[ind])+"\n"
		g.write(AllUsers[ind]+"\t"+str(LiberalProb[ind])+"\t"+str(ConsProb[ind]))	
	else:
		log.write("Another person not considered before is "+user_net.keys()[0]+". This is specially strange\n")
		print "Another person not considered before is "+user_net.keys()[0]+". This is specially strange\n"
		f2=open(file_string2,'a')
		f2.write(user_net.keys()[0]+"\t"+str(0.5)+"\t"+str(0.5)+"\n")
		f2.close()
		g.write(user_net.keys()[0]+"\t"+str(0.5)+"\t"+str(0.5)+"\n")
		
g.close()
f1.close()
log.close()


import smtplib
gmail_user = "danielatemory@gmail.com"
gmail_pwd = "new passwor"
FROM = 'danielatemory@gmail.com'
TO =['dgarci8@emory.edu']
SUBJECT = "Your program has finished running in the server"
TEXT += "Total time:"+str(time.time()-start_time)+"seconds. People updated: "+str(updated)
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
...             """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
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

