import pickle
import re
import collections


def find_winners(tweets, awards, year):
    winners = {}
    win_words = ["win", "won", "wins", "nabs", "takes", "claims", "accepts", "scores", "winner"]
    award_shows = ["Golden Globes", "The Oscars", "The Grammys", "The Tonys", "Academy Awards", "Golden", "Oscars",
                   "Grammys", "Globes", "Golden Globe", "Motion Picture"]
    name_regex = re.compile(r"\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b")
    title_regex = re.compile(r'\b[A-Z][a-z]+\b')
    for award in awards:
        potential_winners = []
        split_award = award.split()
        relevant_tweets = [tweet for tweet in tweets if
                           len(set(split_award).intersection(tweet.split())) >= 4]
        win_tweets = [tweet for tweet in relevant_tweets if any(word in tweet for word in win_words)]
        #win_tweets = [tweet for tweet in tweets if any(word in tweet for word in win_words) and len(set(split_award).intersection(tweet.split())) >= 4]
        if win_tweets:
            relevant_tweets.append(win_tweets)
        for tweet in relevant_tweets:
            people = []
            titles = []
            if isinstance(tweet, str):
                people = name_regex.findall(tweet)
            if people:
                for person in people:
                    name = ' '.join(person)
                    potential_winners.append(name)
            if isinstance(tweet, str):
                titles = title_regex.findall(tweet)
            if titles:
                for title in titles:
                    if not any(title in nom for nom in potential_winners):
                        potential_winners.append(title)

        winner_count = collections.Counter(candidate for candidate in potential_winners if candidate not in award_shows and candidate.lower().split()[0] not in award.split())
        winner = ''
        if winner_count:
            winner = winner_count.most_common(1)[0][0]

        winners[award] = winner

    filename = "winners" + year + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(winners, f)

    return winners


