import networkx as nx
import pandas as pd
import numpy as np
import argparse
import json

def filter_ponies(data):
    not_include = ['ponies','others','and','all']
    #df = pd.read_csv(data)
    df = data.drop(columns=['title','writer'])
    #print(len(df))
    df['pony'] = df['pony'].str.lower()
    for w in not_include:
        df = df[~df.pony.str.contains(w)]
    
    unique_ponies = (df['pony'].value_counts(ascending=False))
    ponies_copy = unique_ponies.copy()
    to_remove = unique_ponies[101:].to_dict()
    unique_ponies = ponies_copy[:101].to_dict()
    for pony in to_remove.keys():
        df = df[df['pony']!=pony]
    #df.to_csv('removed.csv')
    tmp = df['pony'].value_counts()
    tmp.to_csv('tmp.csv')
    #print(df['pony'].value_counts())
    df.to_csv('filter.csv')
    return df, unique_ponies
    
def build_interaction_network(df):
    data, ponies = filter_ponies(df)
    #print(len(data.value_counts()))
    pony_dict = dict.fromkeys(ponies, None)
    G = nx.Graph()
    # for p in ponies:
    #     G.add_node(p)
    # print(len(G))
    for pony in pony_dict:
        pony_dict[pony] = {key:0 for key in pony_dict if (key != pony)}
        #pony_dict[pony]['totalweight'] = 0
    previous = None
    # print('terramar' in ponies)
    for index, row in data.iterrows():
        current = row['pony']
        #print(f'current in ponies: {current, current in ponies}')
        if (current in ponies) & (previous!=current) & (previous!=None):
            pony_dict[current][previous] += 1
            #pony_dict[current]['totalweight'] += 1
        previous = current
    #print(len(pony_dict['twilight sparkle']))
    return pony_dict
#build_interaction_network('/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw9/submission_template/data/clean_dialog.csv')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',help='script-input.csv')
    parser.add_argument('-o',help='interaction-network.json')
    args = parser.parse_args()
    csv_file = args.i
    output = args.o
    df = pd.read_csv(csv_file)
    pony_dict = build_interaction_network(df)
    with open(output, 'w') as f:
        json.dump(pony_dict,f,indent=4)

if __name__ == "__main__":
    main()