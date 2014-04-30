from twython import Twython

CONSUMER_KEY = 'L2i1V237UCGF9Ym5q5eVbw' 
CONSUMER_KEY_SECRET = 'u2ZY7HNX3UCfTuOqCUZ94GiyyCJ7ApmYTxWwCVsSSiE' 
ACCESS_TOKEN = '2176489687-dDxwty9C69p9e9VJuBb4tntswX0PCkOoqUXzwOe'
ACCESS_TOKEN_SECRET = 'fflAmgzvFrCjNtBXX1zufzwpTr8DoToQVM91swjTHZmzv'

f_out = open('tweets.txt','a')

t = Twython(app_key=CONSUMER_KEY, 
            app_secret=CONSUMER_KEY_SECRET, 
            oauth_token=ACCESS_TOKEN, 
            oauth_token_secret=ACCESS_TOKEN_SECRET)

search = t.search(q='#GayMarriage', count=200)
print type(search)
print search.keys()
tweets = search['statuses']



for i in range(0,len(tweets)):
	s1 = tweets[i]['text']
	print s1
	#print '\n\n\n\n'
	#s2 = raw_input("Label? Opposing vs. factual vs. supportive : ")
	#s3 = i,s2,s1.encode('utf8')
	#print s3
	#f_out.write(str(s3))
	#f_out.write('\n')

''' 

tweets = search['statuses']
for tweet in tweets:
	print tweet
	f_out.write(tweet['text'])   
    
   
    

OAuth settings

Your application's OAuth settings. Keep the "Consumer secret" a secret. This key should never be human-readable in your application.

Access level	 Read-only 
About the application permission model
Consumer key	L2i1V237UCGF9Ym5q5eVbw
Consumer secret	u2ZY7HNX3UCfTuOqCUZ94GiyyCJ7ApmYTxWwCVsSSiE
Request token URL	https://api.twitter.com/oauth/request_token
Authorize URL	https://api.twitter.com/oauth/authorize
Access token URL	https://api.twitter.com/oauth/access_token
Callback URL	None
Sign in with Twitter	No
Your access token

Use the access token string as your "oauth_token" and the access token secret as your "oauth_token_secret" to sign requests with your own Twitter account. Do not share your oauth_token_secret with anyone.

Access token	2176489687-dDxwty9C69p9e9VJuBb4tntswX0PCkOoqUXzwOe
Access token secret	fflAmgzvFrCjNtBXX1zufzwpTr8DoToQVM91swjTHZmzv
Access level	Read-only



'''