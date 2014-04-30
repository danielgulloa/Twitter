import json

file_wordprobs = "../Data/BiProbsFromUsers.txt"
file_userwords = "../Data/User_Bi_Dictionary.txt"
file_write="../Data/BiUserProbs_iterated.txt"
file_usersbadbigrams="../Data/UsersWBadBigrams.txt"


AllWords=[]
FirstProb=[]
SecondProb=[]
Count=[]
fWordProbs=open(file_wordprobs,'rb')
for wp in fWordProbs:
	wordprob=wp.strip()
	wordprob=wordprob.split("\t")
	AllWords.append(wordprob[0])
	FirstProb.append(wordprob[1])
	SecondProb.append(wordprob[2])
	Count.append(wordprob[3])
	
Errors=""
UsersWithPoorBigrams=[];

g=open(file_usersbadbigrams,'w')
fWrite=open(file_write,'w')
fUserWords=open(file_userwords,'r')
for line in fUserWords:
	line=line.split(":")
	line1=line[0].split("'")
	user=line1[1]
	line2=line[1].split(",")
	
	for i in range(0,len(line2)):
		line2[i]=line2[i].replace("[","").replace("]","").replace("'","").replace("}","")[1:]
	
	line2[-1]=line2[-1].replace("\n","")
	
	profilewords=line2
	UserProb1=0
	UserProb2=0
	counter=0
	for bigram in profilewords:
		if bigram in AllWords:
			index=AllWords.index(bigram)
			UserProb1+=float(FirstProb[index])
			UserProb2+=float(SecondProb[index])
			counter+=1
				
	if(counter>0):
		fWrite.write(user+"\t"+str(1.0*UserProb1/counter)+"\t"+str(1.0*UserProb2/counter)+"\t"+str(counter)+"\n")
	else:
		g.write(user+"\n")
		Errors+=user+"\n"
		

fWrite.close()
fWordProbs.close()
g.close()


import smtplib
gmail_user = "danielatemory@gmail.com"
gmail_pwd = "new passwor"
FROM = 'danielatemory@gmail.com'
TO =['dgarci8@emory.edu']
SUBJECT = "Your program has finished running in the server"
TEXT = "MakeBiUpdateUsersProb.py produced file BiUserProb_iterated.txt"
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
...             """ % (FROM, ", ".join(TO), SUBJECT, TEXT+Errors)
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





