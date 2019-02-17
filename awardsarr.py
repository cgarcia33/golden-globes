class award(object):
    name = ""
    regex = []
    must = []
    mustnot = []
    ors = []
    awardtype = ""

award1 = award()
award1.name = "cecil b. demille award"
award1.regex = ["Cecil(.*)de(.*)award"]
award1.must = []
award1.mustnot = ["best"]
award1.ors = ["cecil b demille award","cecil b. demille award", "cecil b. de mille award", "cecil b de mille award"]
award1.awardtype = "person"

award2 = award()
award2.name = "best motion picture - drama"
award2.regex = ['Best Motion Picture(.*)Drama', "Best Drama"]
award2.must = ['best', 'drama']
award1.mustnot = ['actor', 'actress', 'television', 'tv', 'series']
award1.ors = []
award1.awardtype = 'movie'

awardarray = [award1, award2]

ceremony_name = "golden globes"