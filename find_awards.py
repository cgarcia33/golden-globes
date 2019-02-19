import pickle


def find_awards(tweets, year):
    award_words = ["best", "award", "actor", "actress", "singer", "drama", "comedy", "song", "performance", "television", "film", "music video", "musical", "movie", "supporting", "series"]
    award_tweets = [tweet for tweet in tweets if len(set(award_words).intersection(tweet.split())) > 3]
    potential_awards = []
    for tweet in award_tweets:
        split_tweet = tweet.split()
        for idx, word in enumerate(split_tweet):
            if word == "best":
                award_name = " ".join([split_tweet[i] for i in range(idx, len(split_tweet))])
                break
        split_award = award_name.split()
        for idx, word in enumerate(reversed(split_award)):
            if word in award_words:
                award_name = " ".join([split_award[i] for i in range(0, len(split_award)-idx)])
                break
        potential_awards.append(award_name)

    awards = set([award.lower() for award in potential_awards if len(award.split()) < 10])

    filename = "awards" + year + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(awards, f)

