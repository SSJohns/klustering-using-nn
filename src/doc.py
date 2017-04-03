from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# random
from random import shuffle

# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import re
import matplotlib.pyplot as plt

docs = {}

class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    item, line = line.split(" : ")
                    # yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
                    docs[item] = line
                    print item
                    yield LabeledSentence(utils.to_unicode(line).split(), [item])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    item, line = line.split(" : ")
                    # self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [item]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

sources = {"../data/sent_tweets.txt": "SENT"}# , "../data/wonderland.txt": "AL"}
sentences = LabeledLineSentence(sources)

model = Doc2Vec(min_count=1, window=7, size=100, sample=1e-4, negative=5, workers=8)

model.build_vocab(sentences.to_array())

for epoch in range(10):
    print("E: ", epoch)
    model.train(sentences.sentences_perm() )
    # model.alpha -= 0.002  # decrease the learning rate
    # model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save('../data/imdb.d2v')

import pprint
pp = pprint.PrettyPrinter(indent=4)
# print("0:")
# pp.pprint(model.docvecs.most_similar(["SENT_0"]))
# print("195:")
# pp.pprint(model.docvecs.most_similar(["SENT_195"]))
# print("226:")
# pp.pprint(model.docvecs.most_similar(["SENT_226"]))

md = 251

X = numpy.empty(shape=(md,100))
for val in docs:
    X[val] = model.docvecs[val]

# tsne = TSNE(n_components=2)
# X_tsne = tsne.fit_transform(X)
# import ipdb; ipdb.set_trace()
kmeans = KMeans(n_clusters=25,random_state=0).fit(X)

# plt.scatter( X_tsne[:, 0], X_tsne[:, 1] )
# for val in range(251):
#     labelv.append("SENT_" + str(val))

from collections import defaultdict
results = defaultdict(list)

for k_label, x, y in zip(kmeans.labels_, X[:, 0], X[:, 1]):
    results[k_label].append(k_label)

for i, v in results.items():
    print i, v

# plt.rcParams["figure.figsize"] = (30,30)
# plt.show()
