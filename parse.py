import json
# parse the tweets 
out = []

with open("Tweets.txt") as f:
    for line in f.readlines():
        line = json.loads(line)
        line = line["text"].encode('utf-8').strip().replace("\n","").lower()
        out.append(line)

with open("sent_tweets.txt", "w") as f:
    for line in out:
        f.write(line)
        f.write("\n")
