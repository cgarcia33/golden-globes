import json
import nltk
import os
from nltk.tokenize import RegexpTokenizer

def getTweets():
    handle = '@goldenglobes'
    handletext = handle[1:]
    jsonData13 = json.loads(open('gg2013.json').read())
    text13 = []
    tokenized13 = []
    official13 = []
    punct13 = []
    tokenizer = RegexpTokenizer(r'\w+')

    for item in jsonData13:
        name = item.get("text")
        text13.append(name)

    for tweet in text13:
        punct13.append(nltk.wordpunct_tokenize(tweet))
        if handle in tweet and 'RT' not in tweet:
            temp = tokenizer.tokenize(tweet)
            if handletext == temp[0]:
                official13.append(temp)
        temp = tokenizer.tokenize(tweet)
        tokenized13.append(temp)
    
    filtered13 = []
    for tweet in official13:
        filterTemp = []
        for token in tweet:
            if token not in stop_words:
                filterTemp.append(token)
        if(filterTemp):
            filtered13.append(filterTemp)
    
    host13 = []
    for tweet in filtered13:
        hostTemp = []
        if 'host' in tweet:
            host13.append(tweet)
        
    tokenString = ""
    tweetString = ""
    for tweet in host13:
        for token in tweet:
            tokenString += token + ' '
        tweetString += tokenString

    #nameregex = re.compile(r'[A-Z][a-zA-Z]*')
    potentialNames = nameregex.findall(tweetString)
    #potentialNames
    list([bigrams(word_tokenize(s)) for s in sent_tokenize(tweetString)])

    #reader = TwitterCorpusReader(root='', fileids='gg2013.json')

def main():
    official13, tokenized13, punct13 = getTweets()
    i = 20

if __name__ == '__main__':
    main()
