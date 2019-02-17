import json
import pandas
from pandas.io.json import json_normalize
import csv
from collections import Counter
import random
import re
import awardsarr


def loadJson(year, t):
    name = 'results/' + year + "/" + t + '.json'
    return json.load(open(name))


def createCSV(year):
    inputname = "gg" + year + ".json"
    outputname = "csvs/tweets" + year + ".csv"
    file = open(inputname, 'r')
    data_json = json.loads(file.read())
    tweets = pandas.DataFrame(json_normalize(data_json)).get("text").tolist()
    with open(outputname, 'w') as resultFile:
        wr = csv.writer(resultFile, quoting=csv.QUOTE_ALL)
        wr.writerow(tweets)


def loadTweets(year):
    name = 'csvs/tweets' + year + '.csv'
    with open(name, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = data[0]
    return data


def removeRT(year):
    data = loadTweets(year)
    tweets = Counter()
    if len(data) > 600000:
        random.shuffle(data)
        data = data[:60000]
    for t in data:
        r = re.findall("RT(?:.*): (.*)", t)
        if r:
            tweets[r[0]] += 1
        else:
            tweets[t] += 1
    with open('countDicts/d' + year + '.json', 'w') as fp:
        json.dump(tweets, fp)


def loadfromJson(year):
    name = 'couintDicts/d' + year + '.json'
    return json.load(open(name))

def awardStopwords():
    name = awardsarr.ceremony_name
    name_words = name.split()
    stops = []
    for nw in name_words:
        stops.append(nw)
        stops.append(nw.capitalize())
        if nw[len(nw)-1] == 's':
            stops.append(nw[:len(nw)-1])
    name = ''.join(name_words)
    stops.append(name)
    return stops


def containsCerName(phrase):
    #name = awardsarr.ceremony_name
    bad_words = awardStopwords()
    for bw in bad_words:
        if bw in phrase:
            return True
    False
