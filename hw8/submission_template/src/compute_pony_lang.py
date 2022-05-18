import argparse
import json
import math
import sys
def get_total_words(data):
    words = 0
    # with open(script,'r') as f:
    #     ponies = json.load(f)
    for i in data.keys():
        words += sum(data[i].values())

def compute_tdidf(word, pony, data):
    # with open(script,'r') as f:
    #     ponies = json.load(f)
    td = data[pony][word]
    freq = 0
    for line in data:
        if word in data[line]:
            freq+=1
    idf = math.log10(6/freq)
    score = td*idf
    return score

def sort_tdidf(data, num_words):
    ponies = {"twilight sparkle": {}, "applejack": {}, "rarity": {}, "pinkie pie": {}, "rainbow dash": {}, "fluttershy": {}}
    for pony,word in data.items():
        for w in word:
            ponies[pony][w] = compute_tdidf(w,pony,data)
    scores = {}
    for pony in ponies.keys():
        p = ponies[pony]
        p = {k:p[k] for k in sorted(p,key = p.get, reverse =True)}
        p = {k:p[k] for k in list(p.keys())[0:int(num_words)]}
        scores[pony] = list(p.keys())
    
    return scores

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',help='pony-counts.json')
    parser.add_argument('-n',help='num-words')
    args = parser.parse_args()

    with open(args.c,'r') as f:
        data = json.load(f)
    
    scores = sort_tdidf(data, args.n)
    json.dump(scores,sys.stdout,indent=4)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
