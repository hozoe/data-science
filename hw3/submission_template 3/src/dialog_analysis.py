import numpy as np
import pandas as pd
import json
import os.path
import sys
from argparse import ArgumentParser

#command line usage: python3 [python program file] [-o] [output json file] [import file]
#df = pd.read_csv("/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw3/clean_dialog.csv")
ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]

def readDF(file):
    df = pd.read_csv((file))
    return df

def getLines(file):
    return len(readDF(file))

def getCount(df):
    d={}
    for p in ponies:
        d[p] = len(df[df['pony'].str.lower()==p])
    return d

def getVerbosity(df,d):
    lines= getLines(df)
    for i,v in d.items():
        d[i] = round(v/lines,2)
    return d

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_csv', help=".csv filename")
    parser.add_argument('-o', metavar='ouput.json')
    args = parser.parse_args()
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, "..", "data", args.input_csv)
    #csv_file = args.input_csv
    csv_file = path
    #print(csv_file)
    json_file = args.o

    count = getCount(readDF(csv_file))
    count_copy = count.copy()
    verbosity = getVerbosity(csv_file, count_copy)
    tojson = {"count":count,"verbosity":verbosity}
    with open('../output.json', 'w') as fp:
        json.dump(tojson, fp, indent=4)

# def main():
#     count = getCount(df)
#     verbosity = getVerbosity(df,count)
#     tojson = {"count":count,"verbosity":verbosity}
#     with open('output.json', 'w') as fp:
#         json.dump(tojson, fp, indent=4)