import json
import argparse
from os import name
import os.path as osp
import pandas as pd
from requests.api import post
import random
def get_json_lines(file):
    lines = 0;
    with open(file) as f:
        for line in f:
            lines+=1
    return lines

def extract_posts(file,numposts,out_file):
    posts=[]
    names = []
    titles = []
    with open(file) as f:
        for line in f:
            post = json.loads(line)
            # name = post['data']['name']
            # title = post['data']['title']
            posts.append(post)
            # names.append(name)
            # titles.append(title)
    #print(len(posts))
    if numposts<=get_json_lines(file):
        posts = random.sample(posts,numposts)
    else:
        posts = random.sample(posts, len(posts))

    for post in posts:
        #print(post)
        names.append(post['data']['name'])
        titles.append(post['data']['title'])
    
    variables = ['Name','title','coding']
    data = pd.DataFrame(columns=variables)
    data['Name'] = names
    data['title'] = titles
    data.to_csv(out_file,sep='\t',index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',help="out-file")
    parser.add_argument('json_file',help="output-file.json")
    parser.add_argument('num_posts',type=int,help='num_posts_to_output')
    args = parser.parse_args()
    extract_posts(args.json_file,args.num_posts,args.o)


if __name__ == "__main__":
    main()



