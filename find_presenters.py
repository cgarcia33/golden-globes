import pickle
import re
import collections


def find_presenters(tweets, awards, year):
    presenters = {}
    present_words = ["present", "presents", "presenting", "read", "reading", "presenter", "presented", "announce", "announces"]
    award_shows = ["Golden Globes", "The Oscars", "The Grammys", "The Tonys", "Academy Awards", "Golden", "Oscars",
                   "Grammys", "Globes", "Golden Globe", "Motion Picture"]
    name_regex = re.compile(r"\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b")
    for award in awards:
        potential_presenters = []
        split_award = award.split()
        relevant_tweets = [tweet for tweet in tweets if
                           len(set(split_award).intersection(tweet.split())) >= 3]
        presenter_tweets = [tweet for tweet in tweets if any(word in tweet for word in present_words) and len(set(split_award).intersection(tweet.split())) >= 3]
        for tweet in presenter_tweets:
            people = []
            if isinstance(tweet, str):
                people = name_regex.findall(tweet)
            if people:
                for person in people:
                    name = ' '.join(person)
                    potential_presenters.append(name)

        potential_presenter_counts = collections.Counter(
            candidate for candidate in potential_presenters if candidate not in award_shows and candidate.lower().split()[0] not in award.split())
        presenter1 = ''
        presenter2 = ''
        presenter_names = []
        if potential_presenter_counts:
            presenter1 = potential_presenter_counts.most_common(1)[-1]
            presenter2 = potential_presenter_counts.most_common(2)[-1]

            if presenter2[1] - presenter1[1] < 20:
                presenter_names = [presenter1[0], presenter2[0]]
            else:
                presenter_names = [presenter1[0]]

        presenters[award] = presenter_names

    filename = "presenters" + year + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(presenters, f)

    return presenters

