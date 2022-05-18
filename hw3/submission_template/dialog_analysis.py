import numpy as np
import pandas as pd
import os
import json
import argparse

df = pd.read_csv("/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw3/clean_dialog.csv") #read file
ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"] #main characters
lines = len(df) #total number of lines

def readfile(path):
    df = pd.read_csv(path)

def getCount(df):
    d={}
    for p in ponies:
        d[p] = len(df[df['pony'].str.lower()==p])
    return d

def getVerbosity(d):
    for i,v in d.items():
        d[i] = round(v/lines,2)
    return d


def main():
    filename = "/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw3/clean_dialog.csv"
    read = readfile(filename)
    count = getCount(df)
    countcopy = count.copy()
    verbosity = getVerbosity(countcopy)
    tojson={"count":count,"verbosity":verbosity}
    #print(tojson)
    with open('output.json', 'w') as fp:
        json.dump(tojson, fp, indent=4)

if __name__ == "__main__":
    main()
