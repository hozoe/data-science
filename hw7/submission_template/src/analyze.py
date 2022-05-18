import argparse
import pandas as pd
import json
import sys
from pandas.core.algorithms import value_counts

def analyze_categories(file):
    data = pd.read_csv(file,delimiter='\t')
    data['coding'] = data['coding'].replace({'c': 'course-related', 'f': 'food-related', 'r': 'residence-related', 'o': 'other'})
    # course = int (data['coding'].value_counts().c)
    # food = int (data['coding'].value_counts().c)
    # res = int (data['coding'].value_counts().r)
    # other = int (data['coding'].value_counts().o)
    # d = {'course-related': course, 'food-related': food, 'residence-related': res, 'other': other}
    #print(data['coding'].value_counts().sort_index())
    return data['coding'].value_counts().to_dict()
    # return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',help='coded-file.tsv')
    parser.add_argument('-o',nargs='?',help='output-file.json')
    args = parser.parse_args()
    #print(analyze_categories('/Users/zoe/Desktop/FALL2021/COMP598/comp598-2021/hw7/submission_template/annotated_mcgill.tsv'))
    dic = analyze_categories(args.i)
    if args.o is not None:
        with open(args.o,'w') as f:
            json.dump(dic,f,indent=4)
    else:
        json.dump(dic,sys.stdout,indent=4)
        sys.stdout.write('\n')

if __name__ == "__main__":
    main()
