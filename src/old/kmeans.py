#Ben Gunning
#Assignment 2
#Professor Wang
import fileinput
import json

"""
*Need to take tweets as inputs into an array
*Need to splice tweets into an array of words
*Need to take each tweet and find Jaccard Distance to centroids; Find minimum and add to cluster
*Need to recompute cluster centroids
*Repeat process until centroids are stable
"""


class KMeans(object):
    def __init__(self, points):
        self.points = points

    def classify(self):
        pass

    def centroids(self, points):
        with open('../data/a2init.txt' , 'r') as centerTxt: # Text file containing IDs of initial selection of centroids
            self.centroid = [] # This stores the IDs of the centroids
            for line in centerTxt:
            	self.centroid.append(int(line[:len(line)-2])) # Read each ID in integer form into the centroid list

    def tweetsIn(self):
        with open('../data/Tweets.txt' , 'r') as tweetsTxt:
            self.tweetsIn = [] # Very raw input of tweets given in the input text
            self.tweetSpl = [] # Dictionary of tweets, each of which is associated with an id number and a list of words (strings)

            for line in tweetTxt:
            	self.tweetsIn.append(json.loads(line))

        for tweet in tweetsIn:
        	id = tweet["id"]
        	words = []
        	for word in tweet["text"].split():
        		words.append(word)
        	self.tweetSpl.append({'id': id , 'words': words}) # Define each tweet as it will be stored in tweetSpl dictionary

    def refine(self):
        isStable = 0
        while isStable == 0:
        	isStable = 1 # Initialize isStable and only remake instability if any of the centroids change
        	clusters = [] # List of list of tweet IDs
        	for cluster in centroid:
        		clusters.append([cluster]) # Append a list, one for each centroid, to the cluster list of lists of tweet IDs
        	for tweet in tweetSpl:
        		if tweet['id'] not in centroid: # If the tweet is not a centroid, it has not been assigned to a list in clusters
        			Jaccard = [] # List of Jaccard distances between a particular tweet and each centroid
        			for cluster in centroid: # cluster would be an ID for a centroid within the centroid list
        				for centerTweet in tweetSpl: # centerTweet would be the tweet in the dictionary belonging to the Id of cluster, in the centroid
        					if cluster == centerTweet['id']: # Match between cluster centroid and the centerTweet's ID
        						intersect = 0
        						for word in tweet['words']:
        							if word in centerTweet['words']:
        								intersect += 1
        						union = len(tweet['words']) + len(centerTweet['words']) - intersect
        				Jaccard.append((union-intersect)/float(union)) # Calculate and add Jaccard value to the list of these values
        			clusters[Jaccard.index(min(Jaccard))].append(tweet['id']) # Find the centroid (cluster) with the minimum Jaccard distance to tweet and add tweet there
        	count = 0
        	for idGroup in clusters: # Recalculate new centroid for each list in our list of lists of IDS (clusters)
        		JaccardList = [] # JaccardList is a list of the sum of all Jaccard distances for each tweet in the idGroup
        		for tweet in idGroup: # tweet will be run for each ID contained within the idGroup
        			for tweetMatch in tweetSpl:
        				if tweet == tweetMatch['id']:
        					tweetJaccard = 0 # tweetJaccard is a sum of the Jaccard distances from tweet to all other tweets in idGroup
        					for otherTweet in idGroup:
        						for tweetinDict in tweetSpl:
        							if otherTweet == tweetinDict['id']:
        								intersect = 0
        								for word in tweetMatch['words']:
        									if word in tweetinDict['words']:
        										intersect += 1
        								union = len(tweetMatch['words']) + len(tweetinDict['words']) - intersect
        								tweetJaccard += (union-intersect)/float(union)
        			JaccardList.append(tweetJaccard)
        		if centroid[count] != idGroup[JaccardList.index(min(JaccardList))]:
        			isStable = 0
        		centroid[count] = idGroup[JaccardList.index(min(JaccardList))]
        		count += 1

        target = open('a2out' , 'w')
        count = 0
        for idGroup in clusters:
        	target.write(str(centroid[count]))
        	target.write(": ")
        	for idNum in idGroup:
        		target.write(str(idNum))
        		target.write(" ")
        	target.write("\n")
        	count += 1
