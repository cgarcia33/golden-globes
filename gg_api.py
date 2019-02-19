'''Version 0.35'''
import json
import pickle
import os
import remove_RT
import find_hosts
import find_awards
import find_nominees
import find_winners
import find_presenters


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best motion picture - comedy or musical',
                        'best performance by an actress in a motion picture - comedy or musical',
                        'best performance by an actor in a motion picture - comedy or musical',
                        'best animated feature film', 'best foreign language film',
                        'best performance by an actress in a supporting role in a motion picture',
                        'best performance by an actor in a supporting role in a motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best original score - motion picture', 'best original song - motion picture',
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
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best performance by an actress in a motion picture - musical or comedy',
                        'best performance by an actor in a motion picture - musical or comedy',
                        'best performance by an actress in a supporting role in any motion picture',
                        'best performance by an actor in a supporting role in any motion picture',
                        'best director - motion picture', 'best screenplay - motion picture',
                        'best motion picture - animated', 'best motion picture - foreign language',
                        'best original score - motion picture', 'best original song - motion picture',
                        'best television series - drama', 'best television series - musical or comedy',
                        'best television limited series or motion picture made for television',
                        'best performance by an actress in a limited series or a motion picture made for television',
                        'best performance by an actor in a limited series or a motion picture made for television',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best performance by an actress in a television series - musical or comedy',
                        'best performance by an actor in a television series - musical or comedy',
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
                        'cecil b. demille award']


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    path = "hosts" + str(year) + ".pkl"
    with open(path, 'rb') as f:
        hosts = pickle.load(f)
    return hosts


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    path = "awards" + str(year) + ".pkl"
    with open(path, 'rb') as f:
        awards = pickle.load(f)
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    path = "nominees" + str(year) + ".pkl"
    with open(path, 'rb') as f:
        nominees = pickle.load(f)
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    path = "winners" + str(year) + ".pkl"
    with open(path, 'rb') as f:
        winners = pickle.load(f)
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    path = "presenters" + str(year) + ".pkl"
    with open(path, 'rb') as f:
        presenters = pickle.load(f)
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
            path = "gg" + year + ".json"
            json_data = json.loads(open(path).read())
            tweets = []
            for item in json_data:
                tweet = item.get("text")
                tweets.append(tweet)
            tweets = remove_RT.remove_RTs(tweets)
            pkl_path = "tweets" + year + ".pkl"
            with open(pkl_path, 'wb') as f:
                pickle.dump(tweets, f)
        except:
            print("JSON file missing")
    print("Pre-ceremony processing complete.")
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
        print(year)
        path = "tweets" + year + ".pkl"
        if os.path.exists(path):
            with open(path, 'rb') as f:
                tweets = pickle.load(f)
            print("finding hosts for " + year)
            hosts = find_hosts.find_hosts(tweets, year)
            print("finding awards for " + year)
            find_awards.find_awards(tweets, year)
            if year == "2013" or year == "2015":
                awards = OFFICIAL_AWARDS_1315
            else:
                awards = OFFICIAL_AWARDS_1819
            print("finding nominees for " + year)
            noms = find_nominees.find_nominees(tweets, awards, year)
            print("finding winners for " + year)
            winners = find_winners.find_winners(tweets, awards, year)
            print("finding presenters for " + year)
            presenters = find_presenters.find_presenters(tweets, awards, year)

            # human readable output
            results_path = year + "results.txt"
            f = open(results_path, 'w')
            if len(hosts) > 1:
                f.write('hosts: ' + ', '.join(hosts) + '\n\n')
            else:
                f.write('host: ' + hosts[0] + '\n')
            for award in awards:
                f.write("Award: " + award + '\n')
                if len(presenters[award]) == 1:
                    f.write("Presenter: " + presenters[award][0] + '\n')
                elif len(presenters[award]) > 1:
                    f.write("Presenters: " + ', '.join(presenters[award]) + '\n')
                else:
                    f.write("Presenter: " + '\n')
                f.write("Nominees: " + ', '.join(noms[award]) + '\n')
                f.write("Winner: " + winners[award] + '\n\n')
            f.close()

            # json output
            results_dict = {}
            results_dict["Host"] = hosts
            for award in awards:
                results_dict[award] = {"Presenters": presenters[award], "Nominees": noms[award], "Winner": winners[award]}
            json_path = year + "results.json"
            with open(json_path, 'w') as fp:
                json.dump(results_dict, fp)
    return


if __name__ == '__main__':
    pre_ceremony()
    main()
