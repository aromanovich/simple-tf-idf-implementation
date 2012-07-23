# coding: utf-8
import re
import string

class Scanner(object):
    _table = re.compile('[%s]' % re.escape(string.punctuation + u'«»…\u2013'))
    
    def __init__(self):
        self._scanner = re.Scanner([
            (r'\S+', lambda _, token: self._table.sub('', token).encode('utf-8')),
            (r'\s+', None)
        ])
    
    def scan(self, s):
        words, remainder = self._scanner.scan(s)
        return words
