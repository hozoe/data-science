import requests
import os.path as osp
import json
import argparse

sample1 = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
sample2 = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']

def get_posts(subred,num_posts=100):
    posts = []
    for sr in subred:
        data=requests.get(f'http://api.reddit.com/r/{sr}/new?limit={num_posts}', headers={'User-Agent': 'windows:requests (by /u/zoe)'})
        content=data.json()['data']['children']
        posts.extend(content)
    return posts

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-o1',required=True,help='outputfile1')
    # parser.add_argument('-o2',required=True,help='outputfile2')
    # args = parser.parse_args()
    file_dir = osp.dirname(__file__)
    # path1 = osp.join(file_dir, '..', 'data', 'sample1.json')
    # path2 = osp.join(file_dir, '..', 'data', 'sample2.json')
    path1 = osp.join(file_dir,'..','sample1.json')
    path2 = osp.join(file_dir,'..','sample2.json')
    with open(path1,'w') as f:
        for line in get_posts(sample1):
            json.dump(line,f)
            f.write('\n')
    
    with open(path2,'w') as f:
        for line in get_posts(sample2):
            json.dump(line,f)
            f.write('\n')


if __name__ == "__main__":
    main()