import json

out = []

with open("../data/Tweets.txt") as f:
    for line in f.readlines():
        line = json.loads(line)
        st = line["id_str"].encode('utf-8')
        line = line["text"].encode('utf-8').strip().replace("\n","").lower()
        out.append( (st, line) )

with open("../data/sent_tweets.txt", "w") as f:
    for line in out:
        f.write(line[0])
        f.write(" : ")
        f.write(line[1])
        f.write("\n")
