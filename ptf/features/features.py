# Copyright  2017  Jian Wang
# License: Apache 2.0.
# Code copied and modified from Kaldi tools
# Copyright  2020  Airenas Vaičiūnas

import sys


# read the features
# return a dict with following items:

#   feats['constant'] is None if there is no constant feature used, else
#                     a 2-tuple (feat_id, value), e.g. (1, 0.01)
#   feats['special'] is a dict whose key is special words and value is a tuple (feat_id, scale)
#   feats['unigram'] is a tuple with (feat_id, entropy, scale)
#   feats['length']  is a tuple with (feat_id, scale)
#
#   feats['match']
#   feats['initial']
#   feats['final']
#   feats['word']    is a dict with key is ngram, value is a tuple (feat_id, scale)
#   feats['min_ngram_order'] is a int represents min-ngram-order
#   feats['max_ngram_order'] is a int represents max-ngram-order
def readFeatures(features_file):
    feats = {}
    feats['constant'] = None
    feats['special'] = {}
    feats['match'] = {}
    feats['initial'] = {}
    feats['final'] = {}
    feats['word'] = {}
    feats['min_ngram_order'] = 10000
    feats['max_ngram_order'] = -1
    feats['len'] = 0
    feat_id = -1

    with open(features_file, 'r', encoding="utf-8") as f:
        for line in f:
            fields = line.split()
            assert (len(fields) in [3, 4, 5])

            feat_id = int(fields[0])
            feat_type = fields[1]
            scale = float(fields[-1])
            if feat_type == 'constant':
                value = float(fields[2])
                feats['constant'] = (feat_id, value)
            elif feat_type == 'special':
                feats['special'][fields[2]] = (feat_id, scale)
            elif feat_type == 'unigram':
                feats['unigram'] = (feat_id, float(fields[2]), scale)
            elif feat_type == 'length':
                feats['length'] = (feat_id, scale)
            elif feat_type in ['word', 'match', 'initial', 'final']:
                ngram = fields[2]
                feats[feat_type][ngram] = (feat_id, scale)
                if feat_type == 'word':
                    continue
                elif feat_type in ['initial', 'final']:
                    order = len(ngram) + 1
                else:
                    order = len(ngram)
                if order > feats['max_ngram_order']:
                    feats['max_ngram_order'] = order
                if order < feats['min_ngram_order']:
                    feats['min_ngram_order'] = order
            else:
                sys.exit(sys.argv[0] + ": error feature type: {0}".format(feat_type))

    feats['len'] = feat_id + 1

    return feats


class Features:
    def __init__(self, features_file):
        self.feats = readFeatures(features_file)

    def len(self):
        return self.feats['len']

    def setWordFeaturesTo(self, word, ans):
        """Return a dict from feat_id to value (as int or float), e.g.
          { 0 -> 1.0, 100 -> 1 }
        """
        feats = self.feats
        if feats['constant'] is not None:
            (feat_id, value) = feats['constant']
            ans[feat_id] = value

        if word in feats['special']:
            (feat_id, scale) = feats['special'][word]
            ans[feat_id] = 1 * scale
            return ans  # return because words with the 'special' feature do
            # not get any other features (except the constant
            # feature).

        if 'unigram' in feats:
            print("Unigram feature is not implemented", file=sys.stderr)
            sys.exit("Unigram feature is not implemented")

        if 'length' in feats:
            (feat_id, scale) = feats['length']
            ans[feat_id] = len(word) * scale

        if word in feats['word']:
            (feat_id, scale) = feats['word'][word]
            ans[feat_id] = 1 * scale

        for pos in range(len(word) + 1):  # +1 for EOW
            for order in range(feats['min_ngram_order'], feats['max_ngram_order'] + 1):
                start = pos - order + 1
                end = pos + 1

                if start < -1:
                    continue

                if start < 0 and end > len(word):
                    # 'word' feature, which we already match before
                    continue
                elif start < 0:
                    ngram_feats = feats['initial']
                    start = 0
                elif end > len(word):
                    ngram_feats = feats['final']
                    end = len(word)
                else:
                    ngram_feats = feats['match']
                if start >= end:
                    continue

                feat = word[start:end]
                if feat in ngram_feats:
                    (feat_id, scale) = ngram_feats[feat]
                    ans[feat_id] += 1 * scale
        return ans
