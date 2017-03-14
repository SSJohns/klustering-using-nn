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
import re
import matplotlib.pyplot as plt

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
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

sources = {"sent_tweets.txt": "SENT"}
sentences = LabeledLineSentence(sources)

model = Doc2Vec(min_count=1, window=15, size=100, sample=1e-4, negative=5, workers=8)

model.build_vocab(sentences.to_array())

for epoch in range(50):
    model.train(sentences.sentences_perm() )
    # model.alpha -= 0.002  # decrease the learning rate
    # model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save('./imdb.d2v')

import pprint
pp = pprint.PrettyPrinter(indent=4)
print("0:")
pp.pprint(model.docvecs.most_similar(["SENT_0"]))
print("195:")
pp.pprint(model.docvecs.most_similar(["SENT_195"]))
print("226:")
pp.pprint(model.docvecs.most_similar(["SENT_226"]))

X = model[model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter( X_tsne[:, 0], X_tsne[:, 1] )
# import ipdb; ipdb.set_trace()
for label, x, y in zip(model.docvecs.doctags.keys(), X_tsne[:, 0], X_tsne[:, 1]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
plt.rcParams["figure.figsize"] = (30,30)
plt.show()
