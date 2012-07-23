# coding: utf-8
import math
import pprint

import cPickle as pickle
from optparse import OptionParser
from collections import defaultdict, OrderedDict

from lemmer import Lemmer


parser = OptionParser()
parser.add_option('-i', '--index', dest='index_path',
                  help='Index file', metavar='FILE')
parser.add_option('-m', '--mystem', dest='mystem_path',
                  help='mystem path', metavar='FILE',
                  default='./mystem')
(options, args) = parser.parse_args()

if options.index_path is None:
    parser.error('Index file is not specified!')


class SearchEngine(object):
    def __init__(self, mystem_path, documents, dictionary):
        self._documents = documents
        self._N = len(documents)
        self._dictionary = dictionary
        self._lemmer = Lemmer(mystem_path)

    def _get_df(self, postings):
        return len(set(postings))

    def _get_top(self, scores):
        result = []
        sorted_scores = sorted(scores.items(), key=lambda (document_id, score): score)
        for (document_id, score) in sorted_scores[-10:]:
            path = self._documents[document_id]
            result.append((path, score))
        return result

    def search(self, *args):
        tfidf = defaultdict(dict)
        query = [self._lemmer.translate(word) for word in args]
        query_dictionary = dict((word, self._dictionary.get(word)) for word in query)

        for (word, postings) in query_dictionary.iteritems():
            df = self._get_df(postings)
            idf = math.log(self._N / float(df))

            for document_id in xrange(self._N):
                tf = query_dictionary[word].count(document_id)
                tfidf[word][document_id] = idf * tf

        scores = {}
        for document_id in xrange(self._N):
            score = 0
            for word in query:
                score += tfidf[word][document_id]
            scores[document_id] = score

        pprint.pprint(self._get_top(scores))


with open(options.index_path, 'rb') as index_file:
    (documents, dictionary) = pickle.load(index_file)
    s = SearchEngine(options.mystem_path, documents, dictionary)
