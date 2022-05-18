import os
import pandas as pd
df = pd.read_csv("/Users/zoe/Desktop/COMP598/comp598-2021/hw1/submission_template/IRAhandle_tweets_1.csv")

# Part 1 - Data Collection

df = df[:10000]
df = df[df["language"]=="English"]
df = df[df["content"].str.contains('\?')==False]
df.to_csv("/Users/zoe/Desktop/COMP598/comp598-2021/hw1/submission_template/collection.tsv", sep='\t')

# Part 2 - Data Annotation
df["trump_mention"] = df["content"].str.contains("(^|[^a-zA-Z0-9])Trump([^a-zA-Z0-9]|$)") #case=False?? 
contains_trump = df["trump_mention"].sum() # number of True's
df["trump_mention"] = df["trump_mention"].map({True:'T', False:'F'})
new_df = df[["tweet_id","publish_date","content","trump_mention"]]
new_df.to_csv("/Users/zoe/Desktop/COMP598/comp598-2021/hw1/submission_template/dataset.tsv", sep='\t', index=False)

# Part 3 - Analysis

trump_stats = contains_trump / len(df["trump_mention"])
final_df = pd.DataFrame({'result': ['frac-trump-mentions'], 'value': ["{:,.3%}".format(trump_stats)]})
final_df.to_csv("/Users/zoe/Desktop/COMP598/comp598-2021/hw1/submission_template/results.tsv", sep='\t', index=False)
print(final_df) #2.249%
