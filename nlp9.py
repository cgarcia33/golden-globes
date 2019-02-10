import json
import nltk
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

nltk.download('stopwords')

def main():
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

    for item in jsonData13:
        text13.append(item.get("text"))
    
    for tweet in text13:
        punct13.append(nltk.wordpunct_tokenize(tweet))
        if 'RT' not in tweet:
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

    #reader = TwitterCorpusReader(root='', fileids='gg2013.json')


if __name__ == '__main__':
    main()

