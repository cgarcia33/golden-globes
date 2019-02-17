
#%%
import json
import nltk
import os
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize, bigrams


#%%
#def load_tweets_from_year(year):
 #   file_string = 'gg' + str(year) + ".json"
  #  tweets = {}
   # with open(file_string, 'r') as f:
    #tweets = json.load(f)


#%%
handle = '@goldenglobes'
handletext = handle[1:]
jsonData13 = json.loads(open('gg2013.json').read())
text13 = []
tokenized13 = []
official13 = []
punct13 = []
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
stop_words.add('goldenglobes')


#%%
for item in jsonData13:
    text13.append(item.get("text"))


#%%
for tweet in text13:
    punct13.append(nltk.wordpunct_tokenize(tweet))
    if 'RT' not in tweet:
        temp = tokenizer.tokenize(tweet)
        if handletext == temp[0]:
            official13.append(temp)
    temp = tokenizer.tokenize(tweet)
    tokenized13.append(temp)


#%%
filtered13 = []
for tweet in official13:
    filterTemp = []
    for token in tweet:
        if token not in stop_words:
            filterTemp.append(token)
    if(filterTemp):
        filtered13.append(filterTemp)

#%% [markdown]
# Find tweets with keyword 'host'

#%%
host13 = []
for tweet in filtered13:
    hostTemp = []
    if 'host' in tweet:
        host13.append(tweet)


#%%
host13


#%%
tokenString = ""
tweetString = ""
for tweet in host13:
    for token in tweet:
        tokenString += token + ' '
    tweetString += tokenString
    
tweetString
    
#nameregex = re.compile(r'[A-Z][a-zA-Z]*')
potentialNames = nameregex.findall(tweetString)
#potentialNames
list([bigrams(word_tokenize(s)) for s in sent_tokenize(tweetString)])


#%%



