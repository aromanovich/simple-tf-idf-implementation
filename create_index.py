import os
import re
import codecs
import string
import subprocess
import fcntl
import select
import cPickle as pickle

from optparse import OptionParser
from collections import defaultdict, OrderedDict

from lemmer import Lemmer
from scanner import Scanner


parser = OptionParser()
parser.add_option('-c', '--collection', dest='collection_dir',
                  help='Collection directory', metavar='DIR')
parser.add_option('-i', '--index', dest='index_path',
                  help='Index file', metavar='FILE')
parser.add_option('-m', '--mystem', dest='mystem_path',
                  help='mystem path', metavar='FILE',
                  default='./mystem')
(options, args) = parser.parse_args()

if options.collection_dir is None:
    parser.error('Collection directory option is required!')

if options.index_path is None:
    parser.error('Index file is not specified!')


def walk(path):
    for root_dir, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root_dir, file)

dictionary = defaultdict(list)
documents = []

lemmer = Lemmer(options.mystem_path)
scanner = Scanner()

for (document_id, document_path) in enumerate(walk(options.collection_dir)):
    with codecs.open(document_path, 'r', 'cp1251') as f:
        words = scanner.scan(f.read())
        for word in words:
            if word:
                stem = lemmer.translate(word)
                dictionary[stem].append(document_id)
        documents.append(document_path)
        print '.',

items = dictionary.items()
items.sort(key=lambda (stem, postings): len(documents))

ordered_dictionary = OrderedDict(items)
index = (documents, ordered_dictionary)

with open(options.index_path, 'wb') as index_file:
    pickle.dump(index, index_file)
