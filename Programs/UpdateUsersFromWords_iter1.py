import json
import time

file_wordprobs = "../Data/WordProbs.txt"
file_userwords = "../Data/User_Words.txt"
file_write="../Data/UserProbs_iterated.txt"
file_write_PoorProfile="../Data/UsersWithPoorProfile.txt"









AllWords=[]
FirstProb=[]
SecondProb=[]
fWordProbs=open(file_wordprobs,'rb')
for wp in fWordProbs:
	wordprob=wp.strip()
	wordprob=wordprob.split("\t")
	AllWords.append(wordprob[0])
	FirstProb.append(wordprob[1])
	SecondProb.append(wordprob[2])

fWordProbs.close()
Text=""
PeopleWithPoorProfile=""
fUserWords=open(file_userwords,'rb')
for line in fUserWords:
	line=line.split(":")
	line1=line[0].split("'")
	user=line1[1]
	line2=line[1].split(",")
	for i in range(0,len(line2)):
		 line2[i]=line2[i].replace("'","")
		 line2[i]=line2[i].replace(" ","")	
	line2[0]=line2[0].replace("[","")
	line2[-1]=line2[-1].replace("]","")
	line2[-1]=line2[-1].replace("\n","")
	profilewords=line2
	UserProb1=0
	UserProb2=0
	counter=0
	flag=False
	for word in profilewords:
		if word in AllWords:
			UserProb1+=float(FirstProb[AllWords.index(word)]);
			UserProb2+=float(SecondProb[AllWords.index(word)]);
			counter+=1
			flag=True	
	if(flag):
		#print user+"\t"+str(1.0*UserProb1/counter)+"\t"+str(1.0*UserProb2/counter)
		Text+=user+"\t"+str(1.0*UserProb1/counter)+"\t"+str(1.0*UserProb2/counter)+"\n"
	else:
		#leave this person with its same probability
		PeopleWithPoorProfile+=line[0].split("'")[1]+"\n"
	


fWrite=open(file_write,'w')
fWrite.write(Text)
fWrite.close()

f=open(file_write_PoorProfile,'w')
f.write(PeopleWithPoorProfile)
f.close()




'''
-------------------
Send Email
------------------
'''

import smtplib
gmail_user = "danielatemory@gmail.com"
gmail_pwd = "new passwor"
FROM = 'danielatemory@gmail.com'
TO =['dgarci8@emory.edu']
SUBJECT = "Your program finished running in the server."
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
...             """ % (FROM, ", ".join(TO), SUBJECT, Text)
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







