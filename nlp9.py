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
    return official13, tokenized13, punct13

def main():
    official13, tokenized13, punct13 = getTweets()
    i = 20

if __name__ == '__main__':
    main()
