import json

f_in = open('sc.test', 'r')
f_out = open('tweets.txt','a')

s=f_in.readlines()



#Parsing 
for key in range(0,27):
	tweet = json.loads(s[key])
	print key
	print (tweet["text"])
	#var = input(" ")	
   



	
f_in.close()
f_out.close()




'''
#These are the keys:
contributors
truncated
text
in_reply_to_status_id
id
favorite_count
source
retweeted
coordinates
entities
in_reply_to_screen_name
id_str
retweet_count
in_reply_to_user_id
favorited
user
geo
in_reply_to_user_id_str
lang
created_at
filter_level
in_reply_to_status_id_str
place



tweet = json.loads(s[1])
print tweet["created_at"]
for key in tweet.keys():
   print key
'''
