from genericpath import exists
import os.path as osp
import json
import argparse
import requests
from bs4 import BeautifulSoup
import hashlib
import os

def get_url(url, cache_dir):
    filename = hashlib.sha1(url.encode('utf-8')).hexdigest()
    path = osp.join(cache_dir, filename)
    if not osp.exists(cache_dir):
        os.makedirs(cache_dir)
    
    content = None
    if not osp.exists(path):
        r = requests.get(url)
        content = r.text
        with open(path,'w') as f:
            f.write(content)
    else:
        content = open(path, 'r').read()
    
    return path

def extract_relationship(file,url):
    relationships = []
    soup = BeautifulSoup(open(file,'r'), 'html.parser')
    status = soup.find('h4', 'ff-auto-status')
    try:
        status_sib = status.next_sibling
    except:
        raise Exception("person dne")       
    candidate = status_sib.find_all('a')
    relationships.extend(get_candidates(candidate,url))

    relationship = soup.find('h4', 'ff-auto-relationships')
    rel_sib = relationship.next_sibling
    while rel_sib is not None and rel_sib.name=="p":
        candidate = rel_sib.find_all('a')
        rel_sib = rel_sib.next_sibling
        rel_sib.find_all('a')
        relationships.extend(get_candidates(candidate,url))
    #print(relationships)
    return relationships
    
    
def get_candidates(candidate_link,person_url):
    relationships = []
    for link in candidate_link:
        if 'href' not in link.attrs:
            continue
        if link['href'].startswith('/dating') and link['href']!=person_url:
            relationships.append(link['href'])
    #print(relationships)
    return relationships

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',required=True,help='config-file.json')
    parser.add_argument('-o',required=True,help='output-file.json')
    args = parser.parse_args()
    config = args.c
    output = args.o
    d = {}
    with open(config,'r') as f:
        cfile = json.load(f)
    cache_dir = osp.join('..',cfile['cache_dir'])
    target_people = cfile['target_people']
    for person in target_people:
        url = 'https://www.whosdatedwho.com/dating/'+person
        person_url = '/dating/'+person
        filename = get_url(url,cache_dir)
        #d[person]= extract_relationship(filename,person_url)
        d[person] = [person.replace('/dating/', '') for person in extract_relationship(filename,person_url)]
        #print(len(d[person]))
    
    with open(output,'w') as f:
        # f.write(
        # '[' +
        # ',\n'.join(json.dumps(i) for i in d) +
        # ']\n')
        json.dump(d,f,indent=4)

if __name__ == "__main__":
    main()
    
    