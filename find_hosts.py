import re
import collections
import pickle


def find_hosts(tweets, year):
    award_shows = ["Golden Globes", "The Oscars", "The Grammys", "The Tonys", "Academy Awards"]
    host_words = ["host", "hosts", "hosting"]
    host_tweets = [tweet for tweet in tweets if any(word in tweet for word in host_words)]
    potential_hosts = []
    name_regex = re.compile(r"\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b")
    for tweet in host_tweets:
        people = name_regex.findall(tweet)
        if people:
            for person in people:
                name = ' '.join(person)
                potential_hosts.append(name)
    potential_host_counts = collections.Counter(candidate for candidate in potential_hosts if candidate not in award_shows)
    host1 = potential_host_counts.most_common(1)[-1]
    host2 = potential_host_counts.most_common(2)[-1]
    if host2[1] - host1[1] < 20:
        hosts = [host1[0], host2[0]]
    else:
        hosts = [host1[0]]

    filename = "hosts" + year + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(hosts, f)

    return hosts
