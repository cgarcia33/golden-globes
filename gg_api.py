'''Version 0.3'''

import json
import helpers
from collections import Counter
import awardsarr
import getawards

OFFICIAL_AWARDS = ['cecil b. demille award',
                   'best motion picture - drama',
                   'best performance by an actress in a motion picture - drama',
                   'best performance by an actor in a motion picture - drama',
                   'best motion picture - comedy or musical',
                   'best performance by an actress in a motion picture - comedy or musical',
                   'best performance by an actor in a motion picture - comedy or musical',
                   'best animated feature film',
                   'best foreign language film',
                   'best performance by an actress in a supporting role in a motion picture',
                   'best performance by an actor in a supporting role in a motion picture',
                   'best director - motion picture',
                   'best screenplay - motion picture',
                   'best original score - motion picture',
                   'best original song - motion picture',
                   'best television series - drama',
                   'best performance by an actress in a television series - drama',
                   'best performance by an actor in a television series - drama',
                   'best television series - comedy or musical',
                   'best performance by an actress in a television series - comedy or musical',
                   'best performance by an actor in a television series - comedy or musical',
                   'best mini-series or motion picture made for television',
                   'best performance by an actress in a mini-series or motion picture made for television',
                   'best performance by an actor in a mini-series or motion picture made for television',
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']



def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    output = helpers.loadJson(year, "hosts")
    hosts = output["hosts"]
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    output = helpers.loadJson(year, "awards")
    awards = output["awards"]
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    output = helpers.loadJson(year, "nominees")
    nominees = output["nominees"]
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    output = helpers.loadJson(year, "winners")
    winners = output["winners"]
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    output = helpers.loadJson(year, "presenters")
    presenters = output["presenters"]
    return presenters



def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    years = ["2013", "2015", "2018", "2019"]
    for year in years:
        try:
            helpers.createCSV(year)
            helpers.removeRT(year)
        except:
            print("Invalid year")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    years = ["2013", "2015", "2018", "2019"]
    for year in years:
        try:
            tweets_dic = helpers.loadfromJson(year)
        except:
            print("Invalid year")
            continue

        hosttweets = {}
        winner_award_tweets = {}
        presenter_counter = Counter()
        tweet_count = len(tweets_dic)
        count = 0
        awards = awardsarr.awardarray

        winners_dict = {}
        presenters_dict = {}
        nominees_dict = {}
        phrases = {}
        best_dressed_counter = Counter()
        worst_dressed_counter = Counter()
        for award in awards:
            winners_dict[award.name] = Counter()
            presenters_dict[award.name] = Counter()
            nominees_dict[award.name] = Counter()
            winner_award_tweets[award.name] = {}

        for tweet in tweets_dic:
            getawards.getRedCarpetInfo(tweet, best_dressed_counter, worst_dressed_counter, tweets_dic[tweet])

        for award in awards:
            if tweet.sorter.sortTweet(tweet, award):
                winner.findWinner(award, tweet, winners_dict[award.name], tweets_dic[tweet], winner_award_tweets[award.name])
                pres.findPresenters(award, tweet, presenters_dict[award.name], tweets_dic[tweet])
                nom.findNominees(award, tweet, nominees_dict[award.name], tweets_dic[tweet])

        #Winners
        final_results = {}
        hosts = hosttest




    return

if __name__ == '__main__':
    main()
