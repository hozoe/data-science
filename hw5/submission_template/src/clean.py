import json
import argparse
import os.path as osp
from datetime import timezone, datetime

# keys = title/title_text; createdAt; text; author; total_count; tags
# only need to remove title and author and total_count if the fields dont meet the requirements
# keep all other records

# part 1 & 2
def format_title(post):
    if "title" in post:
        return post
    elif "title_text" in post:
        post["title"] = post.pop("title_text")
        return post
    elif "title" not in post or "title_text" not in post:
        #print('does not contain title field')
        return None

# part 3 & 4
def createdat_to_utc(post):
    if "createdAt" not in post:
        return post
    
    day = post["createdAt"]
    try:
        time = datetime.strptime(day,"%Y-%m-%dT%H:%M:%S%z")
    except:
        #print("invalid datetime")
        post=None
    else:
        utc_time = datetime.fromtimestamp(time.timestamp(), tz=timezone.utc)
        post["createdAt"] = utc_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return post;

# part 6
def remove_author(post):
    if post["author"]=="N/A" or post["author"]==None:
        return None
    
    elif len(post["author"])==0: #empty
        return None
    else:
        return post

# part 7 & 8
def total_count_to_int(post):
    
    if "total_count" not in post: # if key not present, keep record
        return post

    if (type(post["total_count"]) == int) or (type(post["total_count"]) == float) or (type(post["total_count"]) == str):
        try:
            count = int(post["total_count"])
        except:
            #print("cant cast to int")
            #return None # empty if cant cast
            post = None
        else:
            post["total_count"] = count
    else:
        post = None
    return post
    # if type(post["total_count"]) == int:
    #     return post
    # elif type(post["total_count"]) == float:
    #     count = int(float(post["total_count"]))
    #     post["total_count"] = count
    #     return post
    # elif type(post["total_count"]) == str:
    #     try:
    #         count = int(float(post["total_count"]))
    #     except ValueError as e:
    #         #del post
    #         print("cant cast from str to int")
    #         return None
    #     else:
    #         post["total_count"] = count
    #         return post
    # else:
    #     return None

# part 9
def split_tags(post):
    if "tags" not in post:
        return post

    l = []
    for i in post["tags"]:
        words = i.split()
        if len(words)>1:
            for w in words:
                l.append(w)
        else:
            l.append(i)
    post["tags"] = l
    return post

# part 4 
def valid_json(line):
    try:
        valid = json.loads(line)
    except:
        #print("invalid json dictionaries")
        return None
    else:
        return True
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",required=True, help="input json file")
    parser.add_argument("-o",required=True, help="output json file")

    args = parser.parse_args()
    input = args.i # full path file 
    output = args.o
    if osp.exists(input):
        with open(input, 'r') as file:
            d = []
            for line in file:
                valid = valid_json(line)
                if (valid==True):
                    post = json.loads(line)
                    if format_title(post)==None or remove_author(post)==None or total_count_to_int(post)==None:
                        post=None
                    else:    
                        createdat_to_utc(post)
                        total_count_to_int(post)
                        split_tags(post)
                    if (post!=None):
                        d.append(post)
            # for line in file:
                
            #     try:
            #         valid = json.loads(line)
            #     except:
            #         del line
            #     else:
            #         if format_title(valid)==None or remove_author(valid)==None or total_count_to_int(valid)==None:
            #             valid=None
            #         else:    
            #             createdat_to_utc(valid)
            #             total_count_to_int(valid)
            #             split_tags(valid)
            #         if (valid!=None):
            #             d.append(valid)
            #         #print(d)        
            #print(len(d))
            with open(output,'w') as out:
                for items in d:
                    json.dump(items,out)
                    out.write("\n")
    else:
        print("Error: input file does not exist")

if __name__ == "__main__":
    main()