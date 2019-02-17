import re
import helpers

def getRedCarpetInfo(tweet, best_dressed_counter, worst_dressed_counter, count):
    br = re.findall("(.*) best dressed", tweet, re.IGNORECASE)
    if br:
        br1 = re.findall("((?:[A-Z][a-z]+) (?:[A-Z][a-z]+))", br[0])
        if br1:
            for n in br1:
                if not helpers.containsCerName(n):
                    best_dressed_counter[n] += count