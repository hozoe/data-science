import json
import argparse
import os.path as osp

def read_json(path):
    posts = []
    with open(path, 'r') as json_file:
        for items in json_file:
            d = json.loads(items)
            posts.append(d)
    return posts

def avg_title_length(posts):
    total = 0
    for post in posts:
        total += len(post['data']['title'])

    avg = total / len(posts)
    return avg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',help='input-json-file')
    args = parser.parse_args()
    
    avg = round(avg_title_length(read_json(args.input_file)),2)
    print(avg)

if __name__ == "__main__":
    main()

