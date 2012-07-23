# coding: utf-8
import os
import re
import subprocess
import fcntl
import select


class Lemmer(object):
    _table = re.compile('%s' % re.escape(u'?'))

    def __init__(self, mystem_path):
        self._mystem = subprocess.Popen([mystem_path, '-nlc', '-e utf-8'],
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
        fd = self._mystem.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def __del__(self):
        self._mystem.kill()
    
    def translate(self, word):
        self._mystem.stdin.write(word.strip() + '\n')
        try:
            readable, _, _ = select.select([self._mystem.stdout], [], [], 5e-3)
            readable[0].readline() # skip "\n" line
            stem = readable[0].readline().strip().lower()
            return self._table.sub('', stem).lower()
        except:
            pass
