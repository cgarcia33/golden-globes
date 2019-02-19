def remove_RTs(tweets):
    return [tweet for tweet in tweets if "RT" not in tweet]
