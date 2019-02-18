import json
import nltk
import spacy
import re
from pprint import pprint
from imdb import IMDb
import helpers
import awardsarr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
ia = IMDb()
from collections import Counter

def getWinner(award, t, worddict, count, wintweets):
    if award.awardtype == 'movie':
        y = re.findall("(\".*\") wins best", t, re.IGNORECASE)
        if y and "best" not in y[0].lower():
            title = re.sub(r'[^\w\s]', '', y[0])
            if not helpers.containsCerName(title):
                worddict[title] += count
                if title in wintweets:
                    wintweets[title].append(t)
                else:
                    wintweets[title] = [t]
        w = re.findall("goes to (\".*\")", t, re.IGNORECASE)
        if w:
            title = re.sub(r'[^\w\s]', '', w[0])
            if helpers.containsCerName(title):
                worddict[title] += count
                if title in wintweets:
                    wintweets[title].append(t)
                else:
                    wintweets[title] = [t]
        return
    else:
        keystrings = []
        y = re.final("(.*) wins best", t, re.IGNORECASE)
        if y and not "best" in y[0].lower():
            leftside = y[0]
            leftside = ' '.join(word for word in leftside.split() if word[0]!='#' and not '@' in word and word[0]!= '"')
            y2 = re.findall("((?:[A-Z][a-z]+) (?:[A-Z][-a-zA-Z]+),)", leftside)
            if y2:
                for name in y2:
                    if not helpers.containsCerName(name):
                        keystrings.append(name)
        if len(keystrings) > 0:
            for k in keystrings:
                worddict[k] += count
                if k in wintweets:
                    wintweets[k].append(t)
                else:
                    wintweets[k] = t

def returnWinner(dict):
    maxkey = ''
    maxval = -1
    for k in dict:
        if dict[k] > maxval:
            maxval = dict[k]
            maxkey = k
    return maxkey.lower()

def findPresenters(award, t, names, count):
    presenters = []
    tweets = []
    bytweets = []
    nickname = {}
    nickname['J Lo'] = "Jennifer Lopez"
    nickname["Lo"] = "Jennifer Lopez"
    nickname["Arnold"] = "Arnold Schwarzenegger"
    nickname["Robert Downey"] = "Robert Downey Jr."
    ha = re.findall("(.*)present(?:s|ed|ing)", t, re.IGNORECASE)
    if ha:
        h1 = re.findall("([#@](?:[A-Z][a-z]*)(?:[A-Z][a-z]+))",ha[0])
        if h1:
            for e in h1:
                e = cleanTweet(e,award)
                if e in nickname:
                    e = nickname[e]
                if " " in e:
                    names[e] += count
        h2 = re.findall("((?:[A-Z][-A-Za-z]*)(?:\s[A-Z][-A-Za-z]+))", ha[0])
        if h2:
            for e in h2:
                e = cleanTweet(e,award)
                if e in nickname:
                    e = nickname[e]
                    if e in nickname:
                        e = nickname[e]
                    if " " in e:
                        names[e] += count
    return

def returnNames(tweet, award):
    names = []
    cleaned = cleanTweet(tweet, award)
    nlp = spacy.load('en_core_web_sm')
    if cleaned:
        doc = nlp(cleaned)
        for ent in doc.ents:
            if ent.label_ == "Person":
                names.append(ent.text)
    return names

def cleanTweet(t, award):
    tweet = t
    tweet = tweet.replace('@', "")
    tweet = tweet.replace('#', "")
    r = re.sub ("(?<=\2)([A-Z])", r" \1", tweet)
    if r:
        tweet = " ".join(r.split())
    awardname = award.nane
    stops = set(stopwords.words('english'))
    stops.update(['host', 'hosts', 'hosting', 'rt', 'http', '@', '#', 'movies', 'movie', 'award', 'win', 'wins', '&'])
    stops.update(helpers.awardsStopwords())
    awardwords = ' '.join(re.sub(r"([A-Z])", r" \1", awardname).split())
    awardswords = [word for word in awardwords if word.isalpha()]
    awardwords = [word.lower() for word in awardwords]
    stops.update(awardwords)
    stops.remove(u"and")
    stops.remove(u"or")
    stops.remove(u"don")
    stops.update(['to', "win", "best", "if"])
    tweet = word_tokenize(tweet)
    tweet = [word for word in tweet if word.lower() not in stops]
    return " ".join(tweet)

def findNominees(award, t, keystrings, count):
    r = re.findall("(.*) (?:(?:not win)|(?:is a lock)|(?:should win)|(?: should not win)|(?:better not win)|(?:didn\'t win)|(?:doesn\'t win)|(?:deserves to win)|(?:deserved to win)|(?:better win)|(?:is nominated for)|(?:was nominated for)|(?:will win)|(?:should've won)|(?:could win)|(?:has to win)|(?:is going to win)|(?:is gonna win)|(?:win ))", t, re.IGNORECASE)
    if r and r[0] and "congrat" not in r[0].lower():
        r1 = re.findall("([#@](?:[A-Z][a-z]*)(?:[A-Z][a-z]+))",r[0])
        if r1:
            for e in r1:
                e = cleanTweet(e,award)
                if not e =="":
                    keystrings[e] += count
        if award.awardtype == "movie":
            r2 = re.findall("(\".*\")", r[0])
            if r2:
                e = cleanTweet(r2[0], award)
                if not e == "":
                    keystrings [e] += count

            r3 = re.findall("([A-Z](?:[a-z]+|\.)(?:\s+[A-Z](?:[a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z](?:[a-z]+|\.))",r[0])
            if r3:
                for e in r3:
                    if not e == "":
                        keystrings[e] += count
        else:
            r2 = re.findall("((?:[A-Z][-A-Za-z]*)(?:\s[A-Z][-A-Za-a]+))", r[0])
            if r2:
                for e in r2:
                    if not "golden" in e.lower():
                        keystrings[e] += count
    n = re.findall("Best(.*)nominee ([#@][A-z][a-zA-Z]*)", t, re.IGNORECASE)
    if n:
        keystrings[cleanTweet(n[0][1], award)] += count
    return

def nomineesCounter(c, award):
    atype = award.awardtype
    ndict = Counter()
    for k in c:
        count = c[k]
        if atype == 'movie':
            if len(k.split(" ")) < 7:
                movies = ia.search_movie(k)
                if len(movies) > 0:
                    title = movies[0]["title"]
                    ndict[title] += count
        else:
            if len(k.split (" ")) < 4:
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(k)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        ndict[ent.text] = count
    return ndict