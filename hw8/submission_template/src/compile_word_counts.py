import argparse
import json
from os import remove
from numpy import result_type
import pandas as pd
import re
import os.path as osp

ponies= ['Twilight Sparkle', 'Applejack', 'Rarity', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy']
def get_stopwords(txt_file):
    f = open(txt_file,'r')
    stopwords = f.read().split("\n")
    stopwords = stopwords[6:]
    #print(type(stopwords))
    return stopwords

def preprocess(data,stopwords):
    punctuation = "()[],-.?!:;#&"
    #pony_dict = {"twilight sparkle": {}, "applejack": {}, "rarity": {}, "pinkie pie": {}, "rainbow dash": {}, "fluttershy": {}}
    df = pd.read_csv(data)
    df = df.drop(columns=['title','writer'])
    df = df[df['pony'].isin(ponies)]
    df['dialog'] = df['dialog'].str.replace('[^\w\s]',' ')
    df['dialog'] = df['dialog'].str.lower().str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stopwords))
    #df['dialog'] = df['dialog'].str.lower().str.split(' ').apply(lambda x: ' '.join(j for i, j in enumerate(stopwords) if all(j not in k for k in stopwords[i+1:])))
    
    return df

def compute_counts(data):
    #data['dialog'] = data['dialog'].str.apply(lambda x: ' '.join([word for word in x.split() if word not in (get_stopwords(txt_file))]))
    pony_dict = {'Twilight Sparkle': {}, 'Applejack': {}, 'Rarity': {}, 'Pinkie Pie': {}, 'Rainbow Dash': {}, 'Fluttershy': {}}
    #names = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    for _,r in data.iterrows():
        pony = r['pony']
        dialog = r['dialog']
        words = dialog.split() 
        for word in words:
            if word not in pony_dict[pony]:
                pony_dict[pony][word] = 1
            else:
                pony_dict[pony][word] += 1
    return pony_dict


def keep_frequency(pony_dict):
    names = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    original = ['Twilight Sparkle', 'Applejack', 'Rarity', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy']
    freq = {}
    for pony in pony_dict:
        for word in pony_dict[pony]:
            if word in freq:
                freq[word]+=pony_dict[pony][word]
            else:
                freq[word] = pony_dict[pony][word]
    for word in freq.copy():
        if freq[word]<=4:
            freq.pop(word)
    
    for pony in list(pony_dict):
        for word in list(pony_dict[pony]):
            if word not in freq:
                pony_dict[pony].pop(word)

    result={}
    for i in range(6):
        result[names[i]] = pony_dict.pop(original[i])
    return result
    # for pony,words in list(ponies.items()):
    #     for word, count in list(words.items()):
    #         if(count < threshold):
    #             del ponies[pony][word]
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',help="output-file.json")
    parser.add_argument('-d',help="dialog-file.csv")
    args = parser.parse_args()
    
    #data = pd.read_csv(args.d)
    data = args.d
    stopwords = get_stopwords(osp.join('..','data','stopwords.txt'))
    
    counts = compute_counts(preprocess(data,stopwords))
    res = keep_frequency(counts)
    
    
    with open(args.o,'w+') as f:
        json.dump(res,f)


if __name__ == "__main__":
    main()