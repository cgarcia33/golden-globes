import re
import collections
import pickle


def find_nominees(tweets, awards, year):
    nominees = {}
    nom_words = ["nominated", "nominee"]
    award_shows = ["Golden Globes", "The Oscars", "The Grammys", "The Tonys", "Academy Awards", "Golden", "Oscars", "Grammys", "Globes"]
    for award in awards:
        split_award = award.split()
        relevant_tweets = [tweet for tweet in tweets if len(set(split_award).intersection(tweet.split())) >= 2 and split_award[-1] in tweet]
        nom_tweets = [tweet for tweet in relevant_tweets if any(word in tweet for word in nom_words)]
        relevant_tweets.append(nom_tweets)
        potential_nominees = []
        name_regex = re.compile(r"\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b")
        title_regex = re.compile(r'\b[A-Z][a-z]+\b')
        for tweet in relevant_tweets:
            people = []
            titles = []
            if isinstance(tweet, str):
                people = name_regex.findall(tweet)
                titles = title_regex.findall(tweet)
            if people:
                for person in people:
                    name = ' '.join(person)
                    potential_nominees.append(name)
            if titles:
                for title in titles:
                    if not any(title in nom for nom in potential_nominees):
                        potential_nominees.append(title)

        nom_count = collections.Counter(candidate for candidate in potential_nominees if candidate not in award_shows)
        noms = []
        for nom in nom_count:
            if nom_count[nom] > 10:
                noms.append(nom)

        nominees[award] = noms

    filename = "nominees" + year + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(nominees, f)

    return nominees

