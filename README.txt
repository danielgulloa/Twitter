Documentation for Twitter Sentiment Analysis Project

The goal of the project is to predict build a classification method for two classes (in this case, liberal vs conservative, or supportive towards gay marriage vs opposed) based on the words she uses as well as the friends in her network. We follow the next steps:
---------------------------------------------------------------------
1) Look into the Profiles of 0.5M users for the word "conservative" or "liberal". If they have the word liberal, they are classified as liberals, and viceversa. We could also use their tweets, which are catalogued as supportive towards gay marriage and against (although we only have 1 thousand tweets which were classified by humans), but this has not been yet implemented. On the other hand, only around 4,000 people have these keywords in their profiles, so the initial classification is also very sparse.

Details:
The program DivideByProfile.py takes the file User_Words.txt (which was created with program MakeDictProfiles.py, but this one took a whole weekend to run, even after removing words in the stoplist and punctuation marks. The files created by MakeDictProfiles need to be cleaned: put them in several lines, remove the first { and the last } and sometimes remove spaces between ' . This can be easily done with sed), and creates the file UserProbs.txt. This file has the following format:
user1	1	0
user2	0.5	0.5
...
where the first number is 1 if the user has "liberal" or "liberals" but does not have "conservative" or "conservatives" in their profile. The second number is the analogous for the conservative case. In case it contains both words, or does not contain any of these words, then the probabilities assigned are 0.5 and 0.5. MANY users have these probabilities.

---------------------------------------------------------------------
2) Look into their network, and for each of the 0.5M users, see who they are following.
If they are following many liberals, update the probability of this person to being liberal. Likewise for conservatives. 


Details:
The program Net.txt was done with program SetFriendNetwork.py (runs in about 8 hours) and has the following format:
{userA: {follows:[user2, user3, user4], mutual:[user5], followed_by:[user6, user7]
userB: {follows: [user8, user9], mutual:[], followed_by:[user10, user7]}
}
The program UpdateProbsNetwork.py takes the file Net.txt and looks at the "follows" and "mutual" section of each user. then it looks for, in this case, user2, user3, user4, and user5 in the UserProbs.txt file. The updated probabilities are written to the file UpdatedProbs.txt

Here there are 3 options. I'll replace the users by their probability of being Liberal. For now, it is either 0, 0.5, or 1. It is 0.5 in the case we don't know.
Option1
userA {1 1 0.5 0}  Then P(userA = Liberal) = 2/4.   P(userA=Cons)=1/4     P(userA= ??)=1/4
This option needs to keep track of at least two variables. It could be more accurate, but it leads to very low probabilities for both Liberal and Conservative.

Option2
userA {1 1 0.5 0}  Then P(userA = Liberal)=2/3. P(userA=Cons)=1/3
This would be considering only those probabilities that we actually have. It doesn't take into account how many people she is following, and it could be misleading, since if she is following 666 liberals and 333 conservatives, the probabilities would be the same as in this case.

Option3
userA {1 1 0.5 0} Then P(userA = Liberal)=2.5/4  P(userA=Cons)=1.5/4
In this case, we only need to keep track of one variable. We dont deal with low probabilities. It takes into account how many people are in the network. It assumes that the people we don't know anything about are as likely to be liberals as conservatives.
This is the one we are using.

-------------------------------------------------------------------------------------------
3) Let's go back to the words all users used in their profiles, and assign probabilities to the words themselves of being used by liberals or conservatives.

e.g.
w1 was used by userA, userB, and userC. Their probabilities are 2.5/4, 1/5, 6/10 of being Liberals.  So P(w1 being used by liberals) = (2.5/4+1/5+6/10)/3
and so on for all words.



Details:
The file WordDict.txt (created with program MakeDictProfiles.py) contains a dictionary of all the words used in the profiles, and for each word, who used it. e.g.
w1: [userA, userB, userC]
w2: [userA, userD, userE]
If a word was used only by one user, then we just get rid of it.
This could also be done with BiGrams. the program MakeBiDictProfiles.py (still running (March 12)) is making a file with the same structure but with bigrams instead of just words.


From the UpdatedProbs.txt file, we look for each user, and average the corresponding probabilities. This is done with the program MakeWordProbs.py.
This will create the file WordProbs.txt like
w1	0.75	0.25
w2	0.5	0.5
w3	0.15	0.85

We can also do this with the hashtags. The file Hashtags.txt (made with MakeDictProfiles.py) contains a dictionary of the type
#w1 [user1 user2 user3]
So it is basically the same as WordDict.txt, but only of hashtags. Theoretically, these would provide more information about the probabilities.

----------------------------------------------------------------------------------------------------------
4) Once we have the probabilities for each word (WordProbs.txt  (109 000 words)(again, made with MakeWordProbs.py)), we can go back to the user's profiles and update their probabilities using the word's probabilities.  The file UpdateUsersfromWords_iter1.py creates the file UsersProbs_iterated.txt with the following format:
user1: p1 	1-p1
user2: p2	1-p2
...
  
This file is different and independent from the first file obtained. We can
now join them together, but maybe with some function, instead of just
averaging? Should we just keep this second file since we can argue that it was
obtained based on the first one?


Another problem encountered is that some people have a very poor profile. They
just have their name or their email or something like that. For them, we can't
calculate their probabilities based on their profiles. These people are not
included in the output file, and we have a list of them in the file
UsersWithPoorProfile.txt
The other probabilities are stored in the file UsersProbs_iterated.txt


---------------------------------------------------------------------------------------
5) Now let's repeat the process with bigrams. For each bigram, we give them
probabilities using the probabilities of the users who said them.


Details
BiDict.txt has over 2 million
bigrams. More than unigrams, but most of them are said by only one user. These
will be discarded.
BiDict.txt has the following format:

'w1 w2': [user1 user2 user3]
'w2 w3': [use2 user5]] 
....


Using the file UpdatedProbs.txt (this one has the probabilities of the users
obtained from their network), we estimate the probability of each bigram. The
file MakeBiProbsFromUsers.py creates the file BiProbsFromUsers.txt with the
following format:
'w1 w2'	0.25	0.75	15
'w2 w3'	0.6	0.4	21
...
The third number is the amount of people who said that bigram (it will always
be bigger than 1, because we are eliminating those bigrams said by one person
only (This reduces the amount of bigrams to "only" ~0.5 million))

This has given pretty good results, and I'm thinking of trying trigrams...
e.g.
pro god	0.284615384615	0.715384615385	65
lover nra	0.3125	0.6875	8


---------------------------------------------------------------------------
6) We can go back to updating the probabilities of the users using the
bigrams.  


MakeBiUpdateUsersProb.py  is a program very similar to
UpdateUsersFromWords_iter1.py, but for Bigrams. It creates the file
BiUsersProb.txt with the following format:
user1	prob1	prob2	n
user2	prob1	prob2	n

where n is the number of valid bigrams (bigrams also said by other users) the user had.

----------------------------------------------------------------------------

7) Let's continue where we left off with unigrams (step 4)
We have the file UsersProbs_iterated.txt and we want to calculate back the
probabilities of words
All we need to do is run the file MakeWordProbs_iters.py (very similar to MakeWordProbs.py but change the file
UserProbs.txt to UserProbs_iterated.txt,and removed some stuff from the first
file for sanity check) and this will update the file
WordProbs.txt. I'm also adding the count of people who used that word. Now
WordProbs.txt has this format:

w1	p1	p2	n
w2	p1	p2	n
...


If there are any errors, these will be sent to my email (and printed, but I
might not see them)


----------------------------------
MakeNetDistanceMatrix.py makes the file DistMatrix.csv
user1 \t [list with the number of users that user1 shares with other users]

e.g. user1 follows user20, user31, user42
     user2 follows user31, user88, user144, user520
     user3 follows user20, user42
then DistMatrix.csv:
user1	[3,1,2]
user2	[1,4,0]
user3	[2,0,2]




























