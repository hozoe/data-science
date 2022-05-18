import requests
import argparse
import os.path as osp
import json

def get_posts(subred,num_posts=100):
    posts = []
    data=requests.get(f'http://api.reddit.com/r/{subred}/new?limit={num_posts}', headers={'User-Agent': 'windows:requests (by /u/zoe)'})
    content=data.json()['data']['children']
    posts.extend(content)
    return posts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',help="output-file.json")
    parser.add_argument('-s',help="subreddit")
    args = parser.parse_args()
    out_dir = osp.dirname(__file__)
    out_path = osp.join('..',out_dir,args.o)

    posts = get_posts(args.s,100)
    with open(out_path,'w') as f:
        for line in posts:
            json.dump(line,f)
            f.write('\n')


if __name__ == "__main__":
    main()